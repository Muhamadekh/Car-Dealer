from car_dealer import db, login_manager, app
import jwt
from datetime import datetime, timedelta
from flask_login import UserMixin, current_user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    sale_reference = db.relationship('Car', backref='Owner', lazy=True)
    hire_reference = db.relationship('LendCar', backref='Owner', lazy=True)

    def encode_auth_token(self):
        """
        Generates the Auth Token
        :return: string
        """

        try:
            token = jwt.encode({"user_id": self.id}, app.config['SECRET_KEY'], algorithm="HS256")
            decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            return token, decoded_token
        except Exception as e:
            return e

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String, nullable=False)
    make = db.Column(db.String(50), nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    model = db.Column(db.String(50), nullable=False)
    fuel = db.Column(db.String, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    mfg_year = db.Column(db.Integer, nullable=False)
    engine_size = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    photo = db.Column(db.String(60), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.make}, {self.mileage}, {self.price})'

class LendCar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(40), nullable=False)
    model = db.Column(db.String(40), nullable=False)
    daily_rate = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.String, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    photo = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.model}, {self.daily_rate}'
