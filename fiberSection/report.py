import os
import sys
import reportlab
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import pandas as pd
import sqlite3
import linecache


class Report():
    def __init__(self, controlFile):
        self.controlFile = controlFile
        self.pathname = os.path.dirname(self.controlFile)
        self.FONT_NAME = "GenShinGothic"
        GEN_SHIN_GOTHIC_MEDIUM_TFF = "./font/GenShinGothic-Monospace-Medium.tff"
        pdfmetrics.registerFont(TTFont('GenShinGothic', GEN_SHIN_GOTHIC_MEDIUM_TFF))

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
        comment = df2[0].replace(' ', '')

        c.setFont(self.FONT_NAME, 12)
        c.drawString(55, self.ypos(1, y_shift), title)
        c.setFont(self.FONT_NAME, 9)
        c.drawString(60, self.ypos(3, y_shift), comment,)
        c.drawString(65, self.ypos(4, y_shift), "N=" + nn + "kN,  "\
                                                "θ=" + theta + "deg." \
                )
