import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail


# with open('/etc/config.json') as config_file:
# 	config = json.load(config_file)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ca756c5133bfd45cb5f1ff0c7a21d624'
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = config.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = config.get('EMAIL_PASS')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail(app)


from car_dealer import routes
