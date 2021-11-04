from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField,BooleanField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, Optional
from wtforms.fields.html5 import DateField
from app.database import Category
import datetime

class SignupForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(),DataRequired()])
    password = PasswordField('Password',validators=[ EqualTo('confirm'),DataRequired()])
    confirm = PasswordField('Repeat password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# get categroies for transaction category choices
c = Category.query.all()
categories = []
for i in range(c.__len__()):
    category = (i+1, c[i].name)
    categories.append(category) 

class TransactionForm(FlaskForm):
    name = StringField('Transaction Name', validators=[DataRequired()])
    amount = FloatField('Transaction Amount', validators=[DataRequired()])
    frequency = SelectField('Frequency', choices=[(1, 'Daily'), (2,'Weekly'), (3,'Bi-Weekly'), (4,'Monthly')])
    dow = SelectField('Day of the Week', choices=[(1, 'Monday'),(2,'Tuesday'),(3,'Wednesday'),(4,'Thursday'),(5,'Friday')], validators=[Optional()])
    dom = DateField('Day', format='%Y-%m-%d', validators=[Optional()])
    income = BooleanField('Income?', description='Is this a Deposit or an Expense?', default=False)
    category = SelectField('Category', choices=categories)


class UpdateCurrentB(FlaskForm):
    currentBalance = FloatField('New Current Balance', validators=[DataRequired()])
    password = PasswordField('Confirm Password', validators=[DataRequired()])

class ChangePassword(FlaskForm):
    current_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('Password',validators=[ EqualTo('new_confirm'),DataRequired()])
    new_confirm = PasswordField('Repeat password', validators=[DataRequired()])

