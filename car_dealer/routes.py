import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from car_dealer import app, bcrypt, db
from car_dealer.forms import RegistrationForm, LoginForm, UpdateAccountForm, SellCarForm, LendCarForm
from car_dealer.models import User, Car, LendCar
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    cars = Car.query.all()
    for car in cars:
        print(car.make)
    return render_template('home.html', title='Home Page', cars=cars)


@app.route('/about-us')
def about():
    return render_template('about-us.html', title='About Page')

@app.route('/contact_us')
def contact_us():
    return render_template('contact.html', title='About Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        if user.email == 'root@gmail.com':
            user.is_admin = True
        db.session.commit()
        flash(f'An account has been created for {form.username.data} suscessfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("You have sucessfully logged in", "success")
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash("Please check your email or password", "warning")
        return render_template('login.html', form=form, title='Log in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin:
        # Tables for Users and Cars

        users = User.query.all()
        cars_for_sale = Car.query.all()
        cars_for_hire = LendCar.query.all()

        return render_template('admin.html', title='Account Page', users=users, cars_for_sale=cars_for_sale,
                               cars_for_hire=cars_for_hire)
    else:
        abort(404)


def save_car_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/car_photos', picture_fn)

    output_size = (345, 230)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/sell_car', methods=['GET', 'POST'])
@login_required
def sell_car():
    form = SellCarForm()
    if form.validate_on_submit():
        picture_file = save_car_picture(form.car_photos.data)
        car = Car(make=form.make.data, model=form.model.data, mileage=form.mileage.data, price=form.price.data,
                  user_id=current_user.id, condition=form.condition.data, fuel=form.fuel.data, seats=form.seats.data,
                  mfg_year=form.mfg_year.data,  engine_size=form.engine_size.data, description=form.description.data,
                  photo=picture_file)
        if current_user.is_admin:
            car.is_approved = True
        db.session.add(car)
        db.session.commit()
        if current_user.is_admin:
            flash('You have successfully uploaded your car for sell', 'success')
        else:
            flash('You have uploaded a car for sell. An admin will approve your request shortly.', 'success')
        return redirect(url_for('home'))
    return render_template('sell_car.html', title='Sell a car', form=form)


@app.route('/buy_car', methods=['GET', 'POST'])
def buy_car():
    cars = Car.query.all()
    conditions_list = []
    make_list = []
    model_list = []
    fuel_list = []
    for car in cars:
        if car.is_approved:
            if car.condition not in conditions_list:
                conditions_list.append(car.condition)
            if car.make not in make_list:
                make_list.append(car.make)
            if car.model not in model_list:
                model_list.append(car.model)
            if car.fuel not in fuel_list:
                fuel_list.append(car.fuel)
    return render_template('cars.html', cars=cars, conditions_list=conditions_list, make_list=make_list,
                           model_list=model_list, fuel_list=fuel_list)


@app.route('/car_details')
def car_details():
    return render_template('car-details.html', title='About Page')


@app.route('/livesearch', methods=['GET', 'POST'])
def livesearch():
    search = request.json["text"]
    print(search)
    results = Car.query.filter(Car.make.like(f"{search}%")).all()
    car_objects = []
    for result in results:
        car = {
            "id": result.id,
            "make": result.make,
            "mileage": result.mileage,
            "price": result.price,
            "photo": url_for('static', filename='car_photos/' + result.photo, _external=True),
            "user_id": result.user_id,
            "model": result.model,
            "engine_size": result.engine_size,
            "condition": result.condition,
            "fuel": result.fuel

        }
        car_objects.append(car)

    return jsonify(car_objects)


@app.route('/dropdown_search', methods=['GET', 'POST'])
def dropdown_search():
    selected_term = request.json
    print(selected_term)

    results = Car.query.filter_by(**selected_term).all()
    print(results)
    car_objects = []

    for result in results:
        car = {
            "id": result.id,
            "make": result.make,
            "mileage": result.mileage,
            "price": result.price,
            "photo": url_for('static', filename='car_photos/' + result.photo, _external=True),
            "user_id": result.user_id,
            "model": result.model,
            "engine_size": result.engine_size,
            "condition": result.condition,
            "fuel": result.fuel,
            "description": result.description

        }

        car_objects.append(car)

    return jsonify(car_objects)


@app.route('/lend_car', methods=['GET', 'POST'])
@login_required
def lend_car():
    form = LendCarForm()
    if form.validate_on_submit():
        picture_file = save_car_picture(form.photo.data)
        car = LendCar(brand=form.brand.data, model=form.model.data, daily_rate=form.daily_rate.data, photo=picture_file,
                      fuel=form.fuel.data, seats=form.seats.data, description=form.description.data)
        if current_user.is_admin:
            car.is_approved = True
        db.session.add(car)
        db.session.commit()
        if current_user.is_admin:
            flash('You have uploaded a car for hire', 'success')
        else:
            flash('You have uploaded a car for hire. An admin will approve your request shortly.', 'success')
        return redirect(url_for('home'))
    return render_template('lend_car.html', form=form)


@app.route('/hire_car', methods=['GET', 'POST'])
def hire_car():
    cars = LendCar.query.all()
    brand_list = []
    model_list = []
    fuel_list = []
    for car in cars:
        if car.is_approved:
            if car.brand not in brand_list:
                brand_list.append(car.brand)
            if car.model not in model_list:
                model_list.append(car.model)
            if car.fuel not in fuel_list:
                fuel_list.append(car.fuel)
    return render_template('hire_car.html', cars=cars, brand_list=brand_list, model_list=model_list, fuel_list=fuel_list )


@app.route('/admin/<int:car_id>/car_for_hire', methods=['GET', 'POST'])
def car_hire_info(car_id):
    car_for_hire = LendCar.query.get_or_404(car_id)

    return render_template('car_hire_details.html', car_for_hire=car_for_hire)


@app.route('/admin/<int:car_id>/car_for_sale', methods=['GET', 'POST'])
def car_sales_info(car_id):
    car_for_sale = Car.query.get_or_404(car_id)

    return render_template('car_sales_details.html', car_for_sale=car_for_sale)


@app.route('/approve_car<int:car_id>', methods=['GET', 'POST'])
def approve_car(car_id):
    car_for_sale = Car.query.get_or_404(car_id)
    car_for_hire = LendCar.query.get_or_404(car_id)
    if car_for_sale:
        car_for_sale.is_approved = True
        db.session.add(car_for_sale)
    if car_for_hire:
        car_for_hire.is_approved = True
        db.session.add(car_for_hire)
    db.session.commit()
    flash("You have confirmed this car", "success")
    return redirect(url_for('admin'))
