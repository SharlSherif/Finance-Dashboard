import pandas as pd
import moment
from datetime import timedelta
from datetime import datetime
import seaborn as sns
import matplotlib.pyplot as plt
# ? helpers


def get_difference_between_dates(sdate, edate):
    print(sdate, edate)
    dates_between = []
    [s_year, s_month, s_day] = sdate.split('-')
    [e_year, e_month, e_day] = edate.split('-')
    sdate = datetime(int(s_year), int(s_month), int(s_day))   # start date
    edate = datetime(int(e_year), int(e_month), int(e_day))   # end date

    delta = edate - sdate       # as timedelta

    for i in range(delta.days):
        diff_date = sdate + timedelta(days=i)
        dates_between.append(diff_date)
    # remove first dates in the list because it's the starting date
    if len(dates_between) > 0:
        dates_between.pop(0)
    print(f"{len(dates_between)} dates difference")
    return dates_between


def currency_conversion(amount, currency):
    conversion_rate_USD = 15.6
    converted_amount = 0
    if currency == '$':
        converted_amount = round(amount*conversion_rate_USD)
    else:
        converted_amount = amount
    return converted_amount
# ? helpers


xls = pd.ExcelFile("E:/Projects/Finance-Organizer/finance.xlsx")

file = pd.read_excel(xls, sheet_name="Input", index_col="Date")
from_date = '2020-01-01'  # '2020-01-01'
to_date = '2020-01-07'  # '2020-04-01'


def get_month_data():
    data = file[from_date:to_date]
    conversion_rate_USD = 15.6
    table_income = {}
    accounts = {}
    total_income = 0
    # want to come out with an income table
    for index, row in data.iterrows():
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

    print(accounts)
    bar = {'clients': [], 'amounts': []}
    for key in table_income:
        bar['clients'].append(key)
        bar['amounts'].append(table_income[key])

    print(bar)
    return {'bar': bar, 'accounts': accounts, 'total_income': total_income}


def spending_data(file):
    print("From Date (YYYY-MM-DD):")
    from_date = input()  # '2020-01-01'
    print("To Date (YYYY-MM-DD):")
    to_date = input()  # '2020-04-01'

    data = file[from_date:to_date]
    conversion_rate_USD = 15.6
    table_expenses = {}
    accounts = {}
    total_expenses = 0
    # contains total amount of each day per that date (Month)
    # ? {'DATE':[Sat, Sun, Mon, Tue, Wed, Thu, Fri]}
    # ? {'DATE':[35, 25, 45, 67, 31, 712, 531]}
    heatmap_object = {}
    days = set({})
    last_date_processed = None
    month_name = moment.date('2020-01-01').format('MMMM')
    for date, row in data.iterrows():

        # Filter income only
        if row['Type'] == 'Expense' and row['Category'] != 'Repaid':
            if last_date_processed != None:
                dates_in_between = get_difference_between_dates(
                    str(last_date_processed), (moment.date(date).format('YYYY-MM-DD')))
                for date_in_between in dates_in_between:
                    days.add(moment.date(date_in_between).format('ddd'))
                    date_in_between_formatted = f"{moment.date(date_in_between).format('DD/MM')} ({moment.date(date_in_between).format('dddd')})"
                    heatmap_object[date_in_between_formatted] = 0
            source = row['Comments (Subcategories)']
            account = row['Account']
            description = row['Description']
            expense = currency_conversion(row['Amount'], row['Currency'])
            my_day = date.day
            total_amount_for_day = expense
            for their_date, their_row in data.iterrows():
                # make sure that it's searching only in the "Expenses" row type.
                if their_row['Type'] == 'Expense' and their_date.day == my_day:
                    # perfrom the same operation on currency conversion to get all money in EGP.
                    their_expense = currency_conversion(
                        their_row['Amount'], their_row['Currency'])
                    # addition that expense amount to the total expenses per that day (theyre the same day)
                    total_amount_for_day += their_expense
                    print(f"Date {my_day}, found = ", their_expense)

            print(
                f"Total Amount for Day: {my_day} is {total_amount_for_day} EGP")
            print(date)
            print(moment.date(date).format('ddd'))
            last_date_processed = moment.date(date).format('YYYY-MM-DD')
            # ?day in text (eg. Mon, Sun)
            days.add(moment.date(date).format('ddd'))
            # ? example : 01/01 (Wednesday/Jan)
            date = f"{moment.date(date).format('DD/MM')} ({moment.date(date).format('dddd')})"
            heatmap_object[date] = total_amount_for_day

            total_expenses += expense

    print(heatmap_object)
    print("Total Expenses is ", total_expenses)
    generate_heatmap(heatmap_object, total_expenses)


def generate_heatmap(heatmap_object, total_expenses):
    amounts_splitted_into_arrays = [
        [heatmap_object[key]] for key in heatmap_object]
    bottom_dates = [key for key in heatmap_object]
    array = []
    max_length = 4
    structured = pd.DataFrame(
        amounts_splitted_into_arrays, bottom_dates, [str(total_expenses)+" EGP"])
    plt.figure(figsize=(26, 25))
    plt.title("Spending ")
    ax = sns.heatmap(structured, annot=True, fmt='g', square=True)
    sns.set(font_scale=1.2)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    ax.get_figure().savefig("./heatmap.pdf")


spending_data(file)
