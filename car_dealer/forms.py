from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectField, \
    TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from car_dealer.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username (self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose another one.')

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Login')
    remember = BooleanField('Remember Me')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Upload Profile Photo', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    submit = SubmitField('Upload Photo')

    def validate_username(self, username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('This username is taken. Please choose another one.')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose another one.')


condition_drop_list = ['New', 'Used']
fuel_drop_list = ['Petrol', 'Diesel']
fuel_drop_list = ['Petrol', 'Diesel']
gearbox_drop_list = ['Manual', 'Automatic']


class SellCarForm(FlaskForm):
    condition = SelectField('Car Condition', choices=condition_drop_list, default=1)
    make = StringField('Car Brand, e.g, Toyota, Nissan, etc.', validators=[DataRequired(), Length(min=5, max=20)])
    model = StringField('Car Model, e.g, Premio, Mark X, etc.', validators=[DataRequired(), Length(min=5, max=20)])
    gearbox = SelectField('Gearbox', choices=gearbox_drop_list, default=1)
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    color = StringField('Colour', validators=[DataRequired(), Length(max=10)])
    price = FloatField('Price', validators=[DataRequired()])
    fuel = SelectField('Fuel Type', choices=fuel_drop_list, default=1)
    location = StringField('Location of the car', validators=[DataRequired(), Length(max=30)])
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    mfg_year = IntegerField('Manufacture Year', validators=[DataRequired()])
    engine_size = IntegerField('Engine Size in CC', validators=[DataRequired()])
    description = TextAreaField('Short description', validators=[DataRequired(), Length(min=10, max=140)])
    submit = SubmitField('Next')


class SellCarPhotosForm(FlaskForm):
    car_photos = MultipleFileField('Upload Car Photos', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    submit = SubmitField('Upload')


class LendCarForm(FlaskForm):
    brand = StringField('Car Brand', validators=[DataRequired(), Length(min=3, max=20)])
    model = StringField('Car Model', validators=[DataRequired(), Length(min=3, max=20)])
    daily_rate = IntegerField('Daily Rate', validators=[DataRequired()])
    fuel = SelectField('Fuel Type', choices=fuel_drop_list)
    color = StringField('Colour', validators=[DataRequired(), Length(max=10)])
    gearbox = SelectField('Gearbox', choices=gearbox_drop_list, default=1)
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    location = StringField('Location of the car', validators=[DataRequired(), Length(max=30)])
    description = TextAreaField('Short description', validators=[DataRequired(), Length(min=10, max=140)])
    upload = SubmitField('Next')


class LendCarPhotosForm(FlaskForm):
    car_photos = MultipleFileField('Upload Car Photos', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    submit = SubmitField('Upload')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email (self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("If an account with this email address exists, a password reset message will be sent shortly.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')