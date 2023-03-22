import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify
from car_dealer import app, bcrypt, db
from car_dealer.forms import RegistrationForm, LoginForm, UpdateAccountForm, SellCarForm
from car_dealer.models import User, Car
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home Page')

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
                print("User exist")
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pictures', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You have updated your info', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pictures/' + current_user.image_file)
    return render_template('account.html', form=form, title='Account Page', image_file=image_file)


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
        db.session.add(car)
        db.session.commit()
        flash('Your successfully uploaded your car', 'success')
        return redirect(url_for('home'))
    return render_template('sell_car.html', title='Sell a car', form=form)


@app.route('/buy_car', methods=['GET', 'POST'])
def buy_car():
    cars = Car.query.all()
    return render_template('cars.html', cars=cars)


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



