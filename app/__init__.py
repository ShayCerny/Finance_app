from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'The secret string'
db = SQLAlchemy(app)

from app.database import User, Transaction, Category

lm = LoginManager()
lm.init_app(app)

lm.login_view = 'login'
lm.login_message_category = 'error'

@lm.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from app import routes