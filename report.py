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

# styles
h1 = PS(name='Heading1',
        fontSize=14,
        leading=16)
h2 = PS(name='Heading2',
        fontSize=14,
        leading=16)

class income_report:
    from_date = '2020-01-01'
    to_date = '2020-04-01'
 
    fileName = f'./income_reports/report.{from_date} to {to_date}.pdf'
    pdf = canvas.Canvas(fileName, pagesize=A4)

    def get_month_data(self):
        file = pd.read_excel(
            "E:/Projects/Finance-Organizer/history.xlsx", index_col="Date")
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

        print(accounts)
        bar = {'clients': [], 'amounts': []}
        for key in table_income:
            bar['clients'].append(key)
            bar['amounts'].append(table_income[key])

        print(bar)
        return {'bar': bar, 'accounts': accounts, 'total_income': total_income}

    def draw_income_table(self,accounts_data, total_income):
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
        table = Table(data)

        # add style


        style = TableStyle([
            ('BACKGROUND', (0, 0), (3, 0), colors.HexColor('#c22532')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

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
        
        table.wrapOn(self.pdf, 50*mm, 50*mm)
        table.drawOn(self.pdf, 78*mm, 250*mm)

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
        renderPDF.draw(drawing, self.pdf, 25*mm, 100*mm)

    def draw_paragraphs(self):
        months_selected = Paragraph(f"""
            <para alignment=right>
                <b>{self.from_date}</b>
                <b>{self.to_date}</b>
            </para>
        """, h2)
        months_selected.wrapOn(self.pdf, 50*mm, 50*mm)
        months_selected.drawOn(self.pdf, 5*mm, 275*mm)
        timestamp = Paragraph(
            f"<para alignment=right>{str(datetime.now())}</para>", h2)
        timestamp.wrapOn(self.pdf, 50*mm, 50*mm)
        timestamp.drawOn(self.pdf, 0*mm, 15*mm)

    def generate (self):
        months_data = self.get_month_data()
        self.draw_income_table(months_data['accounts'], months_data['total_income'])
        self.draw_chart_bar(months_data['bar'])
        self.draw_paragraphs()
        self.pdf.save()

report = income_report()
report.generate()