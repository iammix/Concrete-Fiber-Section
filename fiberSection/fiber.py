import math
import openpyxl
from openpyxl.utils import get_column_letter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas
import os

import aijRc
import materials


class Fiber:
    def __init__(self, xx1, xx2, yy1, yy2, material1, material2):
        self.xx1 = xx1
        self.xx2 = xx2
        self.yy1 = yy1
        self.yy2 = yy2
        self.material1 = material1
        self.material2 = material2
        self.position_x = []
        self.position_y = []

        # TODO: not very clear what is the purpose of this loop
        for i in range(len(self.xx1)):
            self.position_x.append(self.xx1[i])
            self.position_y.append(self.yy1[i])

            self.position_x.append(self.xx2[i])
            self.position_y.append(self.yy1[i])

            self.position_x.append(self.xx1[i])
            self.position_y.append(self.yy2[i])

            self.position_x.append(self.xx2[i])
            self.position_y.append(self.yy2[i])
        self.material1 = material1
        self.material2 = material2
        self.material_obj = []
        for index, value in enumerate(self.material1):
            if value == 1:
                self.material_obj.append(materials.ConcNonlinear(self.material2[index]))
            elif value == 2:
                self.material_obj.append(materials.Steel(-99, self.material2[index]))
            elif value == 3:
                self.material_obj.append(materials.ConcEl(self.material2[index]))
            else:
                print("Error: material type not defined")

        self.xnmax = 1.0 * 1.0 ** (-4)
        self.xnmin = - 1.0 * 10 ** (-10)

        self.eps = 1.0
        self.eps2 = 10 ** (-6)

        self.x = []  # x-coordinates position(m)
        self.y = []  # y-coordinates position(m)
        self.r = []  # Rotation
        self.fc = []  # Local stiffness vector
        self.sd = []  # Local area vector
        self.ag = 0  # area

        self.xg = 0
        self.yg = 0
        self.gmax = 0
        self.gmin = 0
        self.error = "Error Occured"

        self.xs = []
        self.ys = []
        self.fy = []
        self.dia = []
        self.ra = []

        self.x_xg = []
        self.y_yg = []
        self.xs_xg = []
        self.ys_yg = []

    def rotation(self, idr, th):
        """
        :param idr: 0 for Compressive fiber
                    1 for Tensile fiber
                    2 for Compressive Bar
                    3 for Tensile Bar
        :param th:
        :return:
        """
        dt = - math.sin(th) * np.array(self.position_x) + math.cos(th) * np.array(self.position_y)
        dtc = - math.sin(th) * np.array(self.x) + math.cos(th) * np.array(self.y)
        dts = - math.sin(th) * np.array(self.xs) + math.cos(th) * np.array(self.ys)
        dt_xg = - math.sin(th) * np.array(self.x_xg) + math.cos(th) * np.array(self.y_yg)

        # TODO: Delete comments in release
        if idr == 0:
            ycc = np.max(dt)
            comment = "Compressive Concrete Fiber: "
        elif idr == 1:
            ycc = np.min(dt)
            comment = "Tensile Concrete Fiber: "
        elif idr == 2:
            ycc = np.max(dts)
            comment = "Compressive Steel Bar: "
        elif idr == 3:
            yyc = np.min(dts)
            comment = "Tensile Steel"
        else:
            comment = "Error strain point in self.rotation(th)"

    def createMatrix(self, xx1, xx2, yy1, yy2, fc, ndimx, ndimy):
        delx = (xx2 - xx1) / float(ndimx)
        dely = (yy2 - yy1) / float(ndimy)
        xx1_b = xx1 + delx / 2.0
        yy1_b = yy1 + dely / 2.0

        for j in range(ndimy):
            for i in range(ndimx):
                self.x.append(float(xx1_b + float(i) * delx))
                self.y.append(float(yy1_b + float(j) * dely))
                self.r.append(float(1))

        da = dely * delx
        for j in range(ndimy):
            for i in range(ndimx):
                self.fc.append(fc)
                self.sd.append(da)

        print("Created Concrete Fiber Prop.")

    def createMatrix_steel(self, xx1, xx2, yy1, yy2, nx, ny, dtx, dty, dia, fy):
        delx = ((xx2 - xx1) - 2.0 * dtx) / (nx - 1.0)
        dely = ((yy2 - yy1) - 2.0 * dty) / (ny - 1.0)

        for i in range(nx):
            self.xs.append(xx1 + dtx + i * delx)
            self.ys.append(yy1 + dty)
            self.dia.append(aijRc.Aij.diameter(dia))
            self.fy.append(fy)
            self.ra.append(aijRc.Aij.rebar_area(dia))

        for i in range(0, nx):
            self.xs.append(xx1 + dtx + i * delx)
            self.ys.append(yy2 - dty)
            self.dia.append(aijRc.Aij.diameter(dia))
            self.fy.append(fy)
            self.ra.append(aijRc.Aij.rebar_area(dia))

        for i in range(0, ny - 2):
            self.xs.append(xx1 + dtx)
            self.ys.append(yy1 + dty + (i + 1) * dely)
            self.dia.append(aijRc.Aij.diameter(dia))
            self.fy.append(fy)
            self.ra.append(aijRc.Aij.rebar_area(dia))

        for i in range(0, ny - 2):
            self.xs.append(xx2 - dtx)
            self.ys.append(yy1 + dty + (i + 1) * dely)
            self.dia.append(aijRc.Aij.diameter(dia))
            self.fy.append(fy)
            self.ra.append(aijRc.Aij.rebar_area(dia))

    def getModel(self, xx1, xx2, yy1, yy2, ndimx, ndimy, fc, ids, nx, ny, dtx, dty, dia, fy):
        try:
            for i in range(len(xx1)):
                self.createMatrix(xx1[i], xx2[i], yy1[i], yy2[i], fc[i], ndimx[i], ndimy[i])
