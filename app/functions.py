from app.database import Category
import calendar, datetime



def get_category_amounts(transactions):
    current_month = datetime.date.today()
    categories = Category.query.all()
    category_amounts = []
    for category in categories:
        amount = 0
        for transaction in transactions:
            if transaction.category == category:
                if transaction.frequency == 4:
                    amount += transaction.amount
                elif transaction.frequency == 3:
                    amount += transaction.amount * 2
                elif transaction.frequency == 2:
                    for week in calendar.monthcalendar(current_month.year, current_month.month):
                        amount += transaction.amount
                elif transaction.frequency == 1:
                    for day in calendar.Calendar().itermonthdays2(current_month.year, current_month.month):
                        if day[0] != 0 and day[1] != 6 or day[1] != 5:
                            amount += transaction.amount
        category_amounts.append(amount)
    return category_amounts


def get_income_expense(transactions):
    current_month = datetime.date.today()
    income = 0
    expense = 0
    for transaction in transactions:
        if transaction.income == True:
            if transaction.frequency == 4:
                income += transaction.amount
            elif transaction.frequency == 3:
                income += transaction.amount * 2
            elif transaction.frequency == 2:
                for week in calendar.monthcalendar(current_month.year, current_month.month):
                    income += transaction.amount
            elif transaction.frequency == 1:
                for day in calendar.Calendar().itermonthdays2(current_month.year, current_month.month):
                    if day[0] != 0 and day[1] != 6 or day[1] != 5:
                        income += transaction.amount
        else:
            if transaction.frequency == 4:
                expense += transaction.amount
            elif transaction.frequency == 3:
                expense += transaction.amount * 2
            elif transaction.frequency == 2:
                for week in calendar.monthcalendar(current_month.year, current_month.month):
                    expense += transaction.amount
            elif transaction.frequency == 1:
                for day in calendar.Calendar().itermonthdays2(current_month.year, current_month.month):
                    if day[0] != 0 and day[1] != 6 or day[1] != 5:
                        expense += transaction.amount
    income_expense = [income, expense]
    return income_expense

def calculate_balance(current_balance, selected_year, selected_month, transactions):
    # Get todays date
    todays_date = datetime.date.today()
    # get days of the current month
    current_month = calendar.Calendar().itermonthdays2(todays_date.year, todays_date.month)
    length_of_month = calendar.monthrange(todays_date.year, todays_date.month)
    # Build month with transactions
    month = []
    for day in current_month:
        new_day = {
            'day': day[0],
            'dow':day[1],
            'transactions':[]
        }
        for transaction in transactions:
            if transaction.frequency == 4:
                if day[0] == transaction.day_of_month.day:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 3:
                if day[0] == 1 or day[0] == 15:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 2:
                if day[1] == transaction.day_of_week:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 1:
                if day[0] != 0:
                    if day[1] != 6 or day[1] != 5:
                        new_day['transactions'].append(transaction)
        month.append(new_day)
    # Finish transactions to end of current month
    end_month_balance = current_balance
    if int(selected_month) > todays_date.month or int(selected_year) > todays_date.year:
        if todays_date.day < length_of_month[1]:
            for i in range(todays_date.day, length_of_month[1]):
                for transaction in month[i]['transactions']:
                    if transaction.income == True:
                        end_month_balance += transaction.amount
                    else:
                        end_month_balance -= transaction.amount
    # find how many months are in between current and selected month
    years = int(selected_year) - todays_date.year
    months = int(selected_month) - todays_date.month
    month_count = months + (years * 12)
    net_monthly = calculateNet(transactions, todays_date)
    # add monthly amount to current balance
    total = 0
    for i in range(1, month_count):
        total += net_monthly
    # return final balance
    final_balance = total + end_month_balance
    return final_balance



def calculateNet(transactions, current_month):
    net = 0
    for transaction in transactions:
        if transaction.frequency == 4:
            if transaction.income == True:
                net += transaction.amount
            else:
                net -= transaction.amount
        elif transaction.frequency == 3:
            if transaction.income == True:
                net += transaction.amount * 2
            else:
                net -= transaction.amount * 2
        elif transaction.frequency == 2:
            if transaction.income == True:
                net += transaction.amount * 4
            else:
                net -= transaction.amount * 4
        elif transaction.frequency == 1:
            for day in calendar.Calendar().itermonthdays2(current_month.year, current_month.month):
                if day[0] != 0 and day[1] != 6 or day[1] != 5:
                    if transaction.income == True:
                        net += transaction.amount
                    else:
                        net -= transaction.amount
    return net


def build_month(year, month, transactions):
    selected_month = calendar.Calendar().itermonthdays2(int(year), int(month))
    month = {
        'days': [],
        'name': datetime.date(int(year), int(month), 1).strftime('%B')
    }
    for day in selected_month:
        new_day = {
            'day': day[0],
            'dow':day[1],
            'transactions':[],
            'balance': 0
        }
        for transaction in transactions:
            if transaction.frequency == 4:
                if day[0] == transaction.day_of_month.day:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 3:
                if day[0] == 1 or day[0] == 15:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 2:
                if day[1] == transaction.day_of_week:
                    new_day['transactions'].append(transaction)
            elif transaction.frequency == 1:
                if day[0] != 0:
                    if day[1] != 6 or day[1] != 5:
                        new_day['transactions'].append(transaction)
        month['days'].append(new_day)
    return month