import pandas as pd
import moment
import math
from datetime import timedelta
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
from helpers import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={
            r"/api/*": {"origins": "*"}})

xls = pd.ExcelFile("E:/Projects/Finance-Organizer/finance.xlsx")

file = pd.read_excel(xls, sheet_name="Input", index_col="Date")


def get_earnings_data(from_date, to_date):
    data = file[from_date:to_date]
    conversion_rate_USD = 15.6
    table_income = {}
    accounts = {}
    table_rows = []
    total_income = 0
    print(data)
    # want to come out with an income table
    for date, row in data.iterrows():
        # Filter income only
        if row['Type'] == 'Income' and row['Category'] != 'Repaid':
            source = row['Comments (Subcategories)']
            account = row['Account']
            income = 0
            if row['Currency'] == '$':
                income = round(row['Amount']*conversion_rate_USD)
            else:
                income = row['Amount']

            total_income += income

            # make a hashtable of income sources (clients) and the income amount associated with them.
            try:
                table_income[source.lower().capitalize(
                )] = table_income[source.lower().capitalize()]+income
            except:
                table_income[source.lower().capitalize()] = income

            # make a hashtable of categories and the income associated with them to put in a bar chart later.
            try:
                accounts[account.lower().capitalize(
                )] = accounts[account.lower().capitalize()]+income
            except:
                accounts[account.lower().capitalize()] = income

            date = f"{moment.date(date).format('DD/MM')} ({moment.date(date).format('dddd')})"

            filtered_row = {}
            collected_row = {
                'Date': date,
                'Client Name': row['Comments (Subcategories)'],
                'Amount': income,
                'Category': row['Category'],
                'Payment Gateway': row['Account'],
                'Description/Notes': row['Description']
            }

            for key in collected_row:
                value = collected_row[key]
                if type(value) != str and isinstance(value, datetime) == False:
                    if math.isnan(value) == False:
                        print(key, value)
                        filtered_row[key] = collected_row[key]
                else:
                    filtered_row[key] = collected_row[key]

            table_rows.append(filtered_row)
    total_income = round(total_income)
    bar = {'clients': [], 'amounts': []}
    for key in table_income:
        bar['clients'].append(key)
        bar['amounts'].append(table_income[key])

    return {'bar': bar, 'accounts': accounts, 'total_income': total_income, 'table': table_rows}


def get_expenses_data(from_date, to_date):
    data = file[from_date:to_date]
    conversion_rate_USD = 15.6
    total_expenses = 0
    categories = []
    sub_categories = []
    table_expenses = {}
    table_rows = []
    # contains total amount of each day per that date (Month)
    # ? {'DATE':[Sat, Sun, Mon, Tue, Wed, Thu, Fri]}
    # ? {'DATE':[35, 25, 45, 67, 31, 712, 531]}
    heatmap_object = {}
    days = set({})
    last_date_processed = None
    # month_name = moment.date('2020-01-01').format('MMMM')
    for date, row in data.iterrows():
        # Filter expenses only
        if row['Type'] == 'Expense' and row['Category'] != 'Repaid':
            if last_date_processed != None:
                dates_in_between = get_difference_between_dates(
                    str(last_date_processed), (moment.date(date).format('YYYY-MM-DD')))
                for date_in_between in dates_in_between:
                    days.add(moment.date(date_in_between).format('ddd'))
                    date_in_between_formatted = f"{moment.date(date_in_between).format('DD/MM')} ({moment.date(date_in_between).format('dddd')})"
                    heatmap_object[date_in_between_formatted] = 0
            sub_category = row['Comments (Subcategories)']
            category = row['Category']
            account = row['Account']
            description = row['Description']
            amount = currency_conversion(row['Amount'], row['Currency'])
            my_day = date.day
            total_amount_for_day = 0
            for their_date, their_row in data.iterrows():
                # make sure that it's searching only in the "Expenses" row type.
                if their_row['Type'] == 'Expense' and their_date.day == my_day:
                    # perfrom the same operation on currency conversion to get all money in EGP.
                    their_expense = currency_conversion(
                        their_row['Amount'], their_row['Currency'])
                    # addition that expense amount to the total expenses per that day (theyre the same day)
                    total_amount_for_day += their_expense
                    print(f"Date {my_day}, found = ", their_expense)

            if total_amount_for_day == 0:
                total_amount_for_day = amount

            if type(sub_category) != str:
                if math.isnan(sub_category) == False:
                    sub_categories.append(sub_category)
                else:
                    sub_categories.append('')
            else:
                sub_categories.append(sub_category)

            categories.append(category)
            print(
                f"Total Amount for Day: {my_day} is {total_amount_for_day} EGP")
            print(moment.date(date).format('ddd'))
            last_date_processed = moment.date(date).format('YYYY-MM-DD')
            # ?day in text (eg. Mon, Sun)
            days.add(moment.date(date).format('ddd'))
            # ? example : 01/01 (Wednesday/Jan)
            date = f"{moment.date(date).format('DD/MM')} ({moment.date(date).format('dddd')})"

            heatmap_object[date] = total_amount_for_day

            try:
                table_expenses[category] += amount
            except:
                table_expenses[category] = amount

            total_expenses += amount

            filtered_row = {}
            collected_row = {
                'Date': date,
                'Category': row['Category'],
                'Amount': amount,
                'Payment Gateway': row['Account'],
                'Comments': row['Comments (Subcategories)'],
                'Description/Notes': row['Description']
            }

            for key in collected_row:
                value = collected_row[key]
                if type(value) != str:
                    if math.isnan(value) == False:
                        print(key, value)
                        filtered_row[key] = collected_row[key]
                else:
                    filtered_row[key] = collected_row[key]

            table_rows.append(filtered_row)

    total_expenses = round(total_expenses)
    print("Total Expenses are ", total_expenses)

    bar = {'categories': [], 'amounts': []}
    for key in table_expenses:
        bar['categories'].append(key)
        bar['amounts'].append(table_expenses[key])

    return {'sub_categories': sub_categories, 'bar': bar, 'table': table_rows, 'total_expenses': total_expenses}


@app.route('/api/earnings', methods=['GET'])
def get_earnings():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    earnings = get_earnings_data(from_date, to_date)
    return earnings


@app.route('/api/expenses', methods=['GET'])
def get_expenses():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    expenses = get_expenses_data(from_date, to_date)
    return expenses


@app.route('/api/dashboard', methods=["GET"])
def get_all_data():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    # calculate these values if found
    percentage_spent =0
    percentage_earned =0
    revenue=0
    # calculate the data
    expenses_data = get_expenses_data(from_date, to_date)
    earnings_data = get_earnings_data(from_date, to_date)
    # calculate additional fields
    total_expenses = expenses_data['total_expenses']
    total_income = earnings_data['total_income']

    if total_expenses > 0 and total_income > 0:
        percentage_spent = round((total_expenses/total_income) * 100)
        percentage_earned = 100-percentage_spent
    
    if total_income > 0:
        revenue = total_income-total_expenses

    return {
        'expenses_data': expenses_data,
        'earnings_data': earnings_data,
        'percentage_earned': percentage_earned,
        'percentage_spent': percentage_spent,
        'revenue': revenue,
        'dates': [moment.date(timestamp).format('YYYY-MM-DD') for timestamp in list(file.index)]
    }
