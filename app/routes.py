from app import app, db
from flask import render_template, flash, redirect, url_for
from app.database import Category, User, Transaction
from app.forms import SignupForm, LoginForm, TransactionForm, UpdateCurrentB, ChangePassword
from flask_login import login_required, login_user, logout_user, current_user
from app.functions import get_category_amounts, get_income_expense, calculate_balance, build_month
import calendar, datetime

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/account')
@login_required
def account():
    user = User.query.filter_by(id=current_user.id).first()
    transactions = Transaction.query.filter_by(user_id = user.id).all()
    category_amounts = get_category_amounts(transactions)
    categories = []
    for category in Category.query.all():
        categories.append(category.name)
    income_expense = get_income_expense(transactions)
    return render_template('account.html', transactions=transactions, categories=categories, category_amounts=category_amounts, income_expense=income_expense)

@app.route('/account/update', methods=['POST','GET'])
@login_required
def update_account():
    form = UpdateCurrentB()
    if form.validate_on_submit():
        if current_user.password == form.password.data:
            current_user.current_balance = form.currentBalance.data
            db.session.commit()
            flash('Balance Updated', 'success')
            return redirect(url_for('account'))
    return render_template('update_account.html', form=form)

@app.route('/account/password', methods=['POST','GET'])
@login_required
def chang_password():
    form = ChangePassword()
    if form.validate_on_submit():
        if current_user.password == form.current_password.data:
            current_user.password = form.new_password.data
            db.session.commit()
            flash('Password has been Changed', 'success')
            return redirect(url_for('account'))        
    return render_template('change_password.html', form=form)

@app.route('/transaction/add', methods=['POST','GET'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        name = form.name.data
        amount = form.amount.data
        frequency = form.frequency.data
        dow = form.dow.data
        dom = form.dom.data
        income = form.income.data
        user_id = current_user.id
        category = form.category.data
        # try:
        new_transaction = Transaction(name=name, amount=amount, frequency=frequency, day_of_week=dow,day_of_month=dom,income=income,user_id=user_id,category_id=category)
        db.session.add(new_transaction)
        db.session.commit()
        flash('Transaction added Successfully', 'success')
        return redirect(url_for('account'))
        # except:
        #     flash('There was an unexpected error, try again', 'error')
    return render_template('add_transaction.html', form=form)

@app.route('/transaction/delete/<id>')
@login_required
def delete_transaction(id):
    transaction = Transaction.query.filter_by(id=id).first()
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted', 'success')
    return redirect(url_for('account'))

@app.route('/picker')
@login_required
def picker():
    # current date
    todays_date = datetime.date.today()
    # Years and months for each year with days of the week after current date up to 3 years out
    years = []
    months = calendar.month_name
    for i in range(0,4):
        years.append(calendar.Calendar().yeardays2calendar(todays_date.year + i, 1))
    return render_template('picker.html', years=years, todays_date=todays_date, months=months)

@app.route('/calendar/<year>/<month>')
@login_required
def calendar_view(year, month):
    # get Todays date
    todays_date = datetime.date.today()
    # Get transactions
    transactions = Transaction.query.filter_by(user_id=current_user.id)
    # Calculate starting balance
    starting_balance = calculate_balance(current_user.current_balance, year, month, transactions)
    # Build selected month
    month_obj = build_month(year, month, transactions)
    # Get a count of empty days that come before the todays date
    exculde_count = 0
    for index, day in enumerate(month_obj['days']):
        if index < todays_date.day:
            if day['day'] == 0:
                exculde_count += 1

    # If selected month is the current month get the number of days to skip for starting balance
    if todays_date.year == int(year) and todays_date.month == int(month):
        exculde_days = (exculde_count - 1) + todays_date.day
    else:
        exculde_days = 0

    for i in range(exculde_days, month_obj['days'].__len__()):
        prev_day = month_obj['days'][i - 1]
        day = month_obj['days'][i]
        if i == exculde_days:
            day['balance'] = starting_balance
        else: 
            day['balance'] = prev_day['balance']
            for transaction in day['transactions']:
                if transaction.income == True:
                    day['balance'] += transaction.amount
                else:
                    day['balance'] -= transaction.amount

    return render_template('calendar.html', month_obj=month_obj, todays_date=todays_date, month=int(month), year=int(year), exculde_count=exculde_count)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            new_user = User(username=username,email=email,password=password)
            db.session.add(new_user)
            db.session.commit()
            flash('Signup Succesfull', 'success')
            return redirect(url_for('login'))
        except:
            flash('There was an unexpected error, try again', 'error')
    return render_template('signup.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username= form.username.data
        user = User.query.filter_by(username=username).first()
        if user:
            if form.password.data == user.password:
                login_user(user)
                flash('Logged in Successfully', 'success')
                return redirect( url_for("index"))
            flash('Incorrect password', 'error')
        else:
            flash('You do not have an account please register.', 'error')
            return redirect(url_for('signup'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))