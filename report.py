import pandas as pd
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.rl_config import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak


def get_month_data():
    file = pd.read_excel(
        "E:/Projects/Finance-Organizer/history.xlsx", index_col="Date")
    data = file['2020-04-01':'2020-04-16']
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
                table_income[source.lower().capitalize()] = table_income[source.lower().capitalize()]+income
            except:
                table_income[source.lower().capitalize()] = income

            # make a hashtable of categories and the income associated with them to put in a bar chart later.
            try:
                accounts[account.lower().capitalize()] = accounts[account.lower().capitalize()]+income
            except:
                accounts[account.lower().capitalize()] = income

    print(accounts)
    bar = {'clients': [], 'amounts': []}
    for key in table_income:
        bar['clients'].append(key)
        bar['amounts'].append(table_income[key])

    print(bar)
    return {'bar': bar, 'accounts': accounts, 'total_income': total_income}


elems = []
fileName = 'pdfTable.pdf'

pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter,
    title="Income Report",
)

# Paragraph("<para alignment='center' fontSize=17 autoLeading=1>Hello World</para>", ParagraphStyle({'alignment':'TA_RIGHT','fontSize':16}))


def generate_income_table(accounts_data, total_income):
    keys = []
    values = []
    for key in accounts_data:
        keys.append(key)
        values.append(str(accounts_data[key]).capitalize() + " EGP")

    keys.append('Total')
    values.append(str(total_income) + " EGP")
    # List of Lists
    data = [
        keys,
        values
    ]

    from reportlab.platypus import Table
    table = Table(data)

    # add style
    from reportlab.platypus import TableStyle
    from reportlab.lib import colors

    style = TableStyle([
        ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#c22532')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),

        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LINEBEFORE', (2, 1), (2, -1), 2, colors.black),
        ('LINEABOVE', (0, 2), (-1, 2), 2, colors.white),

        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d11727')),
    ])
    table.setStyle(style)

    # 2) Alternate backgroud color
    rowNumb = len(data)
    for i in range(1, rowNumb):
        # if i % 2 == 0:
        #     bc = colors.burlywood
        # else:
        #     bc = colors.beige

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), colors.white)]
        )
        table.setStyle(ts)

    # 3) Add borders
    ts = TableStyle(
        [
            ('BOX', (0, 0), (-1, -1), 1, colors.black),

            # ('LINEBEFORE', (2, 1), (2, -1), 2, colors.black),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.white),

            ('GRID', (0, 1), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(ts)
    return table
    # elems.append(table)


month_data = get_month_data()
bar = month_data['bar']
accounts = month_data['accounts']
total_income = month_data['total_income']
income_table = generate_income_table(accounts, total_income)

# sort the amounts by the largest

drawing = Drawing(400, 400)
data = [
    bar['amounts']
]
bc = VerticalBarChart()
bc.x = 50
bc.y = 25
bc.height = 350
bc.width = 350
bc.data = data
bc.strokeColor = colors.black
bc.valueAxis.valueMin = 0
bc.valueAxis.valueStep = 1000
bc.categoryAxis.labels.boxAnchor = 'ne'
bc.categoryAxis.labels.dx = 8
bc.categoryAxis.labels.dy = -2
bc.categoryAxis.labels.angle = 30
bc.categoryAxis.categoryNames = bar['clients']
drawing.add(bc)
h1 = PS(name='Heading1',
                    fontSize=14,
                    leading=16)

elems.append(Paragraph('2020-01-01', h1))
elems.append(Paragraph('2020-04-16', h1))
elems.append(income_table)
elems.append(drawing)

pdf.build(elems)
