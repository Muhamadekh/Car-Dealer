from car_dealer import db, login_manager
from _datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    image_file = db.Column(db.String, nullable=False, default='default.jpg')
    reference = db.relationship('Car', backref='Owner', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    mileage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    photo = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}, {self.mileage}, {self.price})'
