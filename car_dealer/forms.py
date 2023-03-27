from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectField, \
    TextAreaField
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
class SellCarForm(FlaskForm):
    condition = SelectField('Car Condition', choices=condition_drop_list, default=1)
    make = StringField('Car Make, e.g, Toyota, Nissan, etc.', validators=[DataRequired(), Length(min=5, max=20)])
    model = StringField('Car Model, e.g, Premio, Mark X, etc.', validators=[DataRequired(), Length(min=5, max=20)])
    mileage = IntegerField('Mileage', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    fuel = SelectField('Fuel Type', choices=fuel_drop_list, default=1)
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    mfg_year = IntegerField('Manufacture Year', validators=[DataRequired()])
    engine_size = IntegerField('Engine Size', validators=[DataRequired()])
    description = TextAreaField('Short description', validators=[DataRequired(), Length(min=10, max=140)])
    car_photos = FileField('Upload Car Photos', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    submit = SubmitField('Upload')

class LendCarForm(FlaskForm):
    brand = StringField('Car Brand', validators=[DataRequired(), Length(min=5, max=20)])
    model = StringField('Car Model', validators=[DataRequired(), Length(min=5, max=20)])
    daily_rate = IntegerField('Daily Rate', validators=[DataRequired()])
    photo = FileField('Upload Car Photos', validators=[FileAllowed(['jpg', 'png', 'jfif'])])
    fuel = SelectField('Fuel Type', choices=fuel_drop_list)
    seats = IntegerField('Number of Seats', validators=[DataRequired()])
    description = TextAreaField('Short description', validators=[DataRequired(), Length(min=10, max=140)])
    upload = SubmitField('Upload')


