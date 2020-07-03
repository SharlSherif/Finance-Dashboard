import pandas as pd
import moment
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import ParagraphStyle as PS
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import *
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# helper
def format_money(num):
    return '{:,}'.format(num)


# styles
h1 = PS(name='Heading1',
        fontSize=14,
        leading=16)
h2 = PS(name='Heading2',
        fontSize=14,
        leading=16)

small = PS(name='Heading2',
           fontSize=15,
           leading=16)


class income_report:
    print("From Date (YYYY-MM-DD):")
    from_date = input()  # '2020-01-01'
    print("To Date (YYYY-MM-DD):")
    to_date = input()  # '2020-04-01'

    fileName = f'./income_reports/Report - {from_date} to {to_date}.pdf'
    pdf = canvas.Canvas(fileName, pagesize=A4)

    def get_month_data(self):
        xls = pd.ExcelFile("E:/Projects/Finance-Organizer/finance.xlsx")

        file = pd.read_excel(xls,sheet_name="Input", index_col="Date")
        data = file[self.from_date:self.to_date]
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

        bar = {'clients': [], 'amounts': []}
        for key in table_income:
            bar['clients'].append(key)
            bar['amounts'].append(table_income[key])

        print(bar)
        return {'bar': bar, 'accounts': accounts, 'total_income': total_income}

    def draw_income_table(self, accounts_data, total_income):
        keys = []
        values = []
        currency = []
        for key in accounts_data:
            keys.append(key)
            values.append(Paragraph(
                f"<para alignment=center>{format_money(accounts_data[key])}</para>", small))
            currency.append("EGP")

        # append the total earned to the end of the table
        keys.append('Total')
        values.append(Paragraph(
            f"<para alignment=center>{format_money(total_income)}</para>", small))
        currency.append("EGP")

        # List of Lists
        data = [
            keys,
            values,
            currency
        ]
        table = Table(data,)

        # add style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#c22532')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LINEBEFORE', (2, 1), (2, -1), 2, colors.black),
            ('LINEABOVE', (0, 2), (-1, 2), 2, colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 17),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d11727')),
        ])
        table.setStyle(style)

        # 2) Alternate backgroud color
        rowNumb = len(data)
        for i in range(1, rowNumb):
            if i % 2 == 0:
                bc = colors.beige
            else:
                bc = colors.white

            ts = TableStyle(
                [('BACKGROUND', (0, i), (-1, i), bc)]
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

        table.wrapOn(self.pdf, 50*mm, 50*mm)
        table.drawOn(self.pdf, 70*mm, 235*mm)

    def draw_chart_bar(self, bar_data):
        # sort the amounts by the largest
        drawing = Drawing(400, 400)
        data = [
            bar_data['amounts']
        ]
        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 10
        bc.height = 350
        bc.width = 350
        bc.data = data
        bc.strokeColor = colors.black
        bc.valueAxis.valueMin = 0
        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2
        bc.categoryAxis.labels.angle = 30
        bc.categoryAxis.categoryNames = bar_data['clients']
        bc.valueAxis.valueStep = 1000
        drawing.add(bc)
        renderPDF.draw(drawing, self.pdf, 30*mm, 100*mm)

    def draw_paragraphs(self):
        # put months dates top left corner
        months_selected = Paragraph(f"""
            <para alignment=left>
                <b>From {moment.date(self.from_date).format('D/M/YYYY')} ({moment.date(self.from_date).format('dddd, MMMM')})</b>
                <br/>
                <b>To {moment.date(self.to_date).format('D/M/YYYY')} ({moment.date(self.to_date).format('dddd, MMMM')})</b>
            </para>
        """, small)
        months_selected.wrapOn(self.pdf, 120*mm, 50*mm)
        months_selected.drawOn(self.pdf, 15*mm, 275*mm)

        # put timestamp when the report was generated
        timestamp = Paragraph(
            f"""
            <para alignment=left>
                <b>Generated at:</b>
                <br/>
                <br/>
                <p>{moment.now().format('D/M/YYYY')} ({moment.now().format('dddd, MMMM')})</p>
                <br/>
                <p>{moment.now().format('hh:mm:ss A')}</p>
            </para>
            """, h1)
        timestamp.wrapOn(self.pdf, 100*mm, 50*mm)
        timestamp.drawOn(self.pdf, 15*mm, 15*mm)

        # title for the income sources table
        table_title = Paragraph(
            f"""
            <para alignment=center>
                <b>Income Sources</b>
            </para>
            """, h1)
        table_title.wrapOn(self.pdf, 90*mm, 50*mm)
        table_title.drawOn(self.pdf, 62*mm, 263*mm)

    def generate(self):
        months_data = self.get_month_data()
        self.draw_income_table(
            months_data['accounts'], months_data['total_income'])
        self.draw_chart_bar(months_data['bar'])
        self.draw_paragraphs()
        self.pdf.save()


report = income_report()
report.generate()
