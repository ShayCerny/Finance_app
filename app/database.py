from app import db
from flask_login import UserMixin
import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    current_balance = db.Column(db.Float, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.date.today())
    transactions = db.relationship('Transaction', backref='user', lazy=True)


    def __repr__(self):
        return '<User %s %s %s %s>' % (self.username, self.email, self.current_balance, self.last_updated)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Integer, nullable=False) # 1-daily, 2-weekly, 3-biweekly, 4-monthly
    day_of_week = db.Column(db.Integer, nullable=True) # 0-6 Monday-Sunday
    day_of_month = db.Column(db.DateTime, nullable=True)
    income = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='transaction', lazy=True)

    def __repr__(self):
        return '< Transaction %s %s %s>' % (self.name, self.amount, self.frequency)

class Category(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<Category %s>' % self.name


def create_categories():
    categories = ['Bill','Loan','Misc','Grocery','Income','Fun']
    for category in categories:
        new_category = Category(name=category)
        db.session.add(new_category)
    db.session.commit()