import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, jsonify, abort
from car_dealer import app, bcrypt, db, mail
from car_dealer.forms import (RegistrationForm, LoginForm, UpdateAccountForm, SellCarForm, LendCarForm,
                              RequestResetForm, ResetPasswordForm, SellCarPhotosForm, LendCarPhotosForm)
from car_dealer.models import User, Car, LendCar, SellPhotos, HirePhotos
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    car_sale = Car.query.filter_by(is_approved=False).first()
    car_hire = LendCar.query.filter_by(is_approved=False).first()
    cars = Car.query.all()
    cars_photos = {}

    for car in cars:
        car_photo = SellPhotos.query.filter_by(car_id=car.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[car.id] = photo

    return render_template('home.html', title='Home Page', cars=cars, car_sale=car_sale, car_hire=car_hire,
                           cars_photos=cars_photos)


@app.route('/about-us')
def about():
    return render_template('about-us.html', title='About Page')


@app.route('/contact_us', methods=['POST', 'GET'])
@login_required
def contact_us():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        phone = request.form.get('phone')
        msg = f"""
            A message from: {email}
            email: {email}
            phone: {phone}
            message:
            {request.form.get('message')} """
        message = Message('A message from Hirbate Motors', sender='hirbatemotors@gmail.com',
                          recipients=['hirbateahmed@gmail.com'])

        message.body = msg

        mail.send(message)
        flash("Your message has been received! We will get back to you soon. if you need a prompt response please\
                        contact us on +254 723 822 133", "success")

        return redirect(url_for('home'))

    return render_template('contact.html', title='About Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        if user.email == 'hirbatemotors@gmail.com':
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
                flash("You have logged in sucessfully", "success")
                next_page = request.args.get('next')
                if user.is_admin:
                    return redirect(next_page) if next_page else redirect(url_for('admin'))
                else:
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

    form_picture.save(picture_path)

    return picture_fn


@app.route('/sell_car', methods=['GET', 'POST'])
@login_required
def sell_car():
    form = SellCarForm()
    if form.validate_on_submit():
        car = Car(make=form.make.data, model=form.model.data, mileage=form.mileage.data, price=form.price.data,
                  user_id=current_user.id, condition=form.condition.data, fuel=form.fuel.data, seats=form.seats.data,
                  mfg_year=form.mfg_year.data,  engine_size=form.engine_size.data, description=form.description.data,
                  gearbox=form.gearbox.data, color=form.color.data, location=form.location.data)
        if current_user.is_admin:
            car.is_approved = True
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('car_for_sale_photos', car_id=car.id))
    return render_template('sell_car.html', title='Sell a car', form=form)


@app.route('/car_for_sale_photos/<int:car_id>', methods=['GET', 'POST'])
def car_for_sale_photos(car_id):
    form = SellCarPhotosForm()
    if form.validate_on_submit():
        for file in form.car_photos.data:
            picture_file = save_car_picture(file)
            photo = SellPhotos(photos=picture_file, car_id=car_id)
            db.session.add(photo)
            db.session.commit()
        if current_user.is_admin:
            flash('You have successfully uploaded your car for sell', 'success')
        else:
            flash('You have uploaded a car for sell. An admin will approve your request shortly.', 'success')
        return redirect(url_for('home'))
    return render_template('sell_photos.html', title='Upload Car Photos', form=form)


@app.route('/buy_car', methods=['GET', 'POST'])
def buy_car():
    cars = Car.query.all()

    cars_photos = {}
    for car in cars:
        car_photo = SellPhotos.query.filter_by(car_id=car.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[car.id] = photo

    conditions_list = []
    make_list = []
    model_list = []
    fuel_list = []
    seats_list = []
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
            if car.seats not in seats_list:
                seats_list.append(car.seats)
    return render_template('cars.html', cars=cars, conditions_list=conditions_list, make_list=make_list,
                           model_list=model_list, fuel_list=fuel_list, seats_list=seats_list, cars_photos=cars_photos)


@app.route('/car_details<int:car_id>/full_carSale_details')
def car_for_sale_details(car_id):
    user = User.query.filter_by(is_admin=True).first()
    car_for_sale = Car.query.get_or_404(car_id)

    main_photos = []
    extra_photos = []

    car_photo = SellPhotos.query.filter_by(car_id=car_for_sale.id).all()
    if not car_photo:
        photo = 'default.jpeg'
    else:
        main_photos = car_photo[0]
        extra_photos = car_photo[1:]

    return render_template('car_sale_details.html', title='Car Details', car_for_sale=car_for_sale,
                           user=user, main_photos=main_photos, extra_photos=extra_photos)


@app.route('/<int:car_id>/full_carHire_details')
def car_for_hire_details(car_id):
    user = User.query.filter_by(is_admin=True).first()
    car_for_hire = LendCar.query.get_or_404(car_id)

    main_photos = []
    extra_photos = []

    car_photo = HirePhotos.query.filter_by(car_id=car_for_hire.id).all()
    if not car_photo:
        photo = 'default.jpeg'
    else:
        main_photos = car_photo[0]
        extra_photos = car_photo[1:]
    return render_template('car_hire_detail.html', title='About Page', car_for_hire=car_for_hire, user=user,
                           main_photos=main_photos, extra_photos=extra_photos)


@app.route('/livesearch', methods=['GET', 'POST'])
def livesearch():
    search = request.json["text"]
    # print(search)
    results = Car.query.filter(Car.make.like(f"{search}%")).all()
    car_objects = []
    for result in results:
        cars_photos = {}

        car_photo = SellPhotos.query.filter_by(car_id=result.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[result.id] = photo

        car = {
            "id": result.id,
            "make": result.make,
            "mileage": result.mileage,
            "price": result.price,
            "photo": url_for('static', filename='car_photos/' + cars_photos[result.id], _external=True),
            "user_id": result.user_id,
            "model": result.model,
            "engine_size": result.engine_size,
            "condition": result.condition,
            "fuel": result.fuel,
            "description": result.description,
            "seats": result.seats,
            "gearbox": result.gearbox,
            "mfg_year": result.mfg_year

        }
        car_objects.append(car)

    return jsonify(car_objects)


def check_term(selected_term):
    terms_dict = {k:v for k,v in selected_term.items() if k in ['condition', 'make', 'model', 'fuel', 'seats']}
    results = Car.query.filter_by(**terms_dict).all()
    if "price" in selected_term:
        value_list = [int(value) for value in selected_term['price'].split(',')]
        min_price = value_list[0]
        max_price = value_list[1]
        price_results = Car.query.filter(Car.price.between(min_price, max_price)).all()
        results = list(set(results).intersection(set(price_results)))
    if "mileage" in selected_term:
        value_list = [int(value) for value in selected_term['mileage'].split(',')]
        min_mileage = value_list[0]
        max_mileage = value_list[1]
        mileage_results = Car.query.filter(Car.mileage.between(min_mileage, max_mileage)).all()
        results = list(set(results).intersection(set(mileage_results)))
    if "engine_size" in selected_term:
        value_list = [int(value) for value in selected_term['engine_size'].split(',')]
        min_engine_size = value_list[0]
        max_engine_size = value_list[1]
        engine_results = Car.query.filter(Car.engine_size.between(min_engine_size, max_engine_size)).all()
        results = list(set(results).intersection(set(engine_results)))
    return results


@app.route('/dropdown_search', methods=['GET', 'POST'])
def dropdown_search():
    selected_term = request.json

    output = check_term(selected_term)

    car_objects = []

    for result in output:

        cars_photos = {}

        car_photo = SellPhotos.query.filter_by(car_id=result.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[result.id] = photo

        car = {
            "id": result.id,
            "make": result.make,
            "mileage": result.mileage,
            "price": result.price,
            "photo": url_for('static', filename='car_photos/' + cars_photos[result.id], _external=True),
            "user_id": result.user_id,
            "model": result.model,
            "engine_size": result.engine_size,
            "condition": result.condition,
            "fuel": result.fuel,
            "description": result.description,
            "seats": result.seats,
            "gearbox": result.gearbox,
            "mfg_year": result.mfg_year

        }
        car_objects.append(car)

    return jsonify(car_objects)


def check_hire_term(selected_term):
    terms_dict = {k: v for k, v in selected_term.items() if k in ['brand', 'model', 'fuel', 'seats']}
    results = LendCar.query.filter_by(**terms_dict).all()
    if "daily_rate" in selected_term:
        value_list = [int(value) for value in selected_term['daily_rate'].split(',')]
        min_rate = value_list[0]
        max_rate = value_list[1]
        rate_results = LendCar.query.filter(LendCar.daily_rate.between(min_rate, max_rate)).all()
        results = list(set(results).intersection(set(rate_results)))
    return results


@app.route('/car_hire_search', methods=['GET', 'POST'])
def car_hire_search():
    selected_term = request.json
    print(selected_term)
    search_results = check_hire_term(selected_term)

    car_objects = []

    for result in search_results:

        cars_photos = {}

        car_photo = HirePhotos.query.filter_by(car_id=result.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[result.id] = photo

        car = {
            "id": result.id,
            "make": result.brand,
            "mileage": result.gearbox,
            "daily_rate": result.daily_rate,
            "photo": url_for('static', filename='car_photos/' + cars_photos[result.id], _external=True),
            "user_id": result.user_id,
            "model": result.model,
            "fuel": result.fuel,
            "description": result.description,
            "seats": result.seats

        }
        car_objects.append(car)

    return jsonify(car_objects)


@app.route('/lend_car', methods=['GET', 'POST'])
@login_required
def lend_car():
    form = LendCarForm()
    if form.validate_on_submit():
        car = LendCar(brand=form.brand.data, model=form.model.data, daily_rate=form.daily_rate.data, fuel=form.fuel.data,
                      seats=form.seats.data, description=form.description.data, color=form.color.data,
                      user_id=current_user.id, gearbox=form.gearbox.data, location=form.location.data)
        if current_user.is_admin:
            car.is_approved = True
        db.session.add(car)
        db.session.commit()
        return redirect(url_for('car_for_hire_photos', car_id=car.id))
    return render_template('lend_car.html', form=form)


@app.route('/car_for_hire_photos/<int:car_id>', methods=['GET', 'POST'])
def car_for_hire_photos(car_id):
    form = LendCarPhotosForm()
    if form.validate_on_submit():
        for file in form.car_photos.data:
            picture_file = save_car_picture(file)
            photo = HirePhotos(photos=picture_file, car_id=car_id)
            db.session.add(photo)
            db.session.commit()
        if current_user.is_admin:
            flash('You have successfully uploaded your car for hire', 'success')
        else:
            flash('You have uploaded a car for hire. An admin will approve your request shortly.', 'success')
        return redirect(url_for('home'))
    return render_template('hire_photos.html', title='Upload Car Photos', form=form)


@app.route('/hire_car', methods=['GET', 'POST'])
def hire_car():
    cars = LendCar.query.all()

    cars_photos = {}

    for car in cars:
        car_photo = HirePhotos.query.filter_by(car_id=car.id).first()
        if not car_photo:
            photo = 'default.jpeg'
        else:
            photo = car_photo.photos
        cars_photos[car.id] = photo

    brand_list = []
    model_list = []
    fuel_list = []
    seats_list = []
    for car in cars:
        if car.is_approved:
            if car.brand not in brand_list:
                brand_list.append(car.brand)
            if car.model not in model_list:
                model_list.append(car.model)
            if car.fuel not in fuel_list:
                fuel_list.append(car.fuel)
            if car.seats not in seats_list:
                seats_list.append(car.seats)
    return render_template('hire_car.html', cars=cars, brand_list=brand_list, model_list=model_list,
                           seats_list=seats_list, fuel_list=fuel_list, cars_photos=cars_photos)


@app.route('/<int:car_id>/car_for_hire', methods=['GET', 'POST'])
def car_hire_info(car_id):
    car_for_hire = LendCar.query.get_or_404(car_id)

    cars_photos = {}

    car_photo = HirePhotos.query.filter_by(car_id=car_id).first()
    if not car_photo:
        photo = 'default.jpeg'
    else:
        photo = car_photo.photos
    cars_photos[car_for_hire.id] = photo

    return render_template('car_hire_info.html', car_for_hire=car_for_hire, cars_photos=cars_photos)


@app.route('/<int:car_id>/car_for_sale', methods=['GET', 'POST'])
def car_sales_info(car_id):
    car_for_sale = Car.query.get_or_404(car_id)

    cars_photos = {}

    car_photo = SellPhotos.query.filter_by(car_id=car_id).first()
    if not car_photo:
        photo = 'default.jpeg'
    else:
        photo = car_photo.photos
    cars_photos[car_for_sale.id] = photo

    return render_template('car_sales_info.html', car_for_sale=car_for_sale, cars_photos=cars_photos)


@app.route('/approve_car<int:car_id>/car_for_sale', methods=['GET', 'POST'])
def approve_car_for_sale(car_id):
    car_for_sale = Car.query.get_or_404(car_id)
    car_for_sale.is_approved = True
    db.session.commit()
    flash("You have confirmed this car", "success")
    return redirect(url_for('admin'))


@app.route('/approve_car<int:car_id>/car_for_hire', methods=['GET', 'POST'])
def approve_car_for_hire(car_id):
    car_for_hire = LendCar.query.get_or_404(car_id)
    car_for_hire.is_approved = True
    db.session.commit()
    flash("You have confirmed this car", "success")
    return redirect(url_for('admin'))


@app.route('/car_for_sale/<int:car_id>/delete_car', methods=['POST'])
def delete_car_for_sale(car_id):
    car = Car.query.get_or_404(car_id)
    photos = SellPhotos.query.filter_by(car_id=car.id).all()
    for photo in photos:
        db.session.delete(photo)
    db.session.delete(car)
    db.session.commit()
    flash("You have deleted this car.", "danger")
    return redirect(url_for('admin'))

@app.route('/car_for_hire/<int:car_id>/delete_car', methods=['POST'])
def delete_car_for_hire(car_id):
    car = LendCar.query.get_or_404(car_id)
    photos = HirePhotos.query.filter_by(car_id=car.id).all()
    for photo in photos:
        db.session.delete(photo)
    db.session.delete(car)
    db.session.commit()
    flash("You have deleted this car.", "danger")
    return redirect(url_for('admin'))


def send_reset_email(user):
    token = User.get_reset_token(user)
    msg = Message('Password Reset Request', sender='hirbatemotors@gmail.com', recipients=[user.email])

    msg.body = f""" To reset your password, visit the following link.
{url_for('reset_token', token=token, _external=True)}   

if you did not make this request, please ignore this message and your details will remain the same.
   
"""
    mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email with instructions has been sent to your email.", "info")
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
