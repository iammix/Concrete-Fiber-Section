import os
import sys
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm

import pandas as pd

GEN_SHIN_GOTHIC_MEDIUM_TTF = "./fonts/GenShinGothic-Monospace-Medium.ttf"


class Report():
    def __init__(self, cntlfile):
        self.cntlFile = cntlfile
        self.pathname = os.path.dirname(self.cntlFile)
        # self.FONT_NAME = "Helvetica"
        self.FONT_NAME = "GenShinGothic"
        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TTF))

    def create_row(self, c, index, df, df2, index2):
        y_shift = -360 * index
        c.setFont(self.FONT_NAME, 9)
        mc_x = "{:10.0f}".format(df.iloc[0, 1])
        mc_y = "{:10.0f}".format(df.iloc[0, 2])
        ma_x = "{:10.0f}".format(df.iloc[1, 1])
        ma_y = "{:10.0f}".format(df.iloc[1, 2])
        mu_x = "{:10.0f}".format(df.iloc[2, 1])
        mu_y = "{:10.0f}".format(df.iloc[2, 2])

        title = str(df2[0])
        theta = str(df2[2])
        nn = str(df2[3])
        comment = df2[8].replace(' ', '')

        # Model
        c.setFont(self.FONT_NAME, 12)
        c.drawString(55, self.ypos(1, y_shift),
                     title \
                     )
        c.setFont(self.FONT_NAME, 9)
        c.drawString(60, self.ypos(3, y_shift),
                     comment, \
                     )
        c.drawString(65, self.ypos(4, y_shift),
                     "N=" + nn + "kN,  " \
                                 "θ=" + theta + "deg." \
                     )

        # Design Condition
        c.setFont(self.FONT_NAME, 9)

        c.drawString(55, self.ypos(27, y_shift),
                     "Capacity:" \
                     )
        c.drawString(60, self.ypos(29, y_shift),
                     "Mcx = " + mc_x + " kN.m" \
                     )
        c.drawString(60, self.ypos(30, y_shift),
                     "Max = " + ma_x + " kN.m" \
                     )
        c.drawString(60, self.ypos(31, y_shift),
                     "Mux = " + mu_x + " kN.m" \
                     )

        c.drawString(180, self.ypos(29, y_shift),
                     "Mcy = " + mc_y + " kN.m" \
                     )
        c.drawString(180, self.ypos(30, y_shift),
                     "May = " + ma_y + " kN.m" \
                     )
        c.drawString(180, self.ypos(31, y_shift),
                     "Muy = " + mu_y + " kN.m" \
                     )
        imagefile = self.pathname + "/" + df2.iloc[13].replace(' ', '') + "mp.png"
        c.drawImage(imagefile, 300, y_shift + 345, width=9 * cm, preserveAspectRatio=True, mask='auto')
        imagefile = self.pathname + "/" + df2.iloc[13].replace(' ', '') + "model.png"
        c.drawImage(imagefile, 50, y_shift + 150, width=7.5 * cm, preserveAspectRatio=True, mask='auto')

    def ypos(self, ipos, y_shift):
        return 730 - (ipos - 1) * 10 + y_shift

    def print_page(self, c, index, nCase):
        c.setFont(self.FONT_NAME, 20)
        c.drawString(50, 795, u"Fiber Analysis")
        xlist = [40, (40 + 560) / 2, 560]
        ylist = [760, 780]
        c.grid(xlist, ylist)

        # sub title
        c.setFont(self.FONT_NAME, 12)
        c.drawString(55, 765, u"Model")
        c.drawString(315, 765, u"M-φ Relationship")
        for i in range(0, nCase):
            df2 = pd.read_csv(self.cntlFile)
            df2 = df2.iloc[i + index, :]
            table = self.pathname + "/" + df2.iloc[13].replace(' ', '') + "cap"
            df = pd.read_csv(table)
            data = df
            self.create_row(c, i, data, df2, index)
        ylist = [40, 400, 760]
        c.grid(xlist, ylist[2 - nCase:])
        c.showPage()

    def print_head(self, c, title):
        c.setFont(self.FONT_NAME, 20)
        c.drawString(50, 795, title)

        c.setFont(self.FONT_NAME, 12)
        inputf = './db/input.txt'
        f = open(inputf, 'r', encoding='utf-8')
        tmpData = []
        while True:
            line = f.readline()
            if line:
                if line != '\n':
                    tmpData.append(line.replace('\n', ''))
                else:
                    tmpData.append('')
            else:
                break
        f.close()
        data = tmpData
        # c.setFont(self.FONT_NAME, 9)
        for i in range(0, len(data)):
            # txt
            c.drawString(55, 720 - (i - 1) * 14, data[i])
        c.showPage()

    def create_pdf(self, dataNum, pdfFile, title):
        c = canvas.Canvas(pdfFile)

        numPage = dataNum // 2
        numMod = dataNum % 2
        # print(numPage,numMod)
        if numMod >= 1:
            numPage = numPage + 1

        for i in range(0, numPage):
            index = 2 * i  # index: 参照データのインデックス
            if numPage == 1:
                self.print_page(c, index, dataNum)
            elif i != numPage - 1 and numPage != 1:
                self.print_page(c, index, 2)
            else:
                if numMod != 0:
                    self.print_page(c, index, numMod)
                else:
                    self.print_page(c, index, 2)

        c.save()
        print("repot.py is Okay!!.")



########################################################################
# test script

pathname = "./test.pdf"
obj = Report()

########################################################################
inputf = []
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")
inputf.append("./db/rcslab.txt")

title = "sample"
