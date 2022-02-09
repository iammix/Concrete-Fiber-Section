import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class Concrete_ParabolicLinearEC2:
    def __init__(self, e:float):
        self.e = e



class ConcEl:
    def __init__(self, sig_b):
        self.es = 4700.0 * math.sqrt(sig_b)
        self.ea = sig_b / self.es

    def sig_c(self, e):
        if e >= 0.0:
            return self.es * e
        else:
            return self.es * e / 1000.0

    def ecs(self, sig_s):
        return sig_s / self.es

    def test(self):
        x = np.arange(-2.0 * self.ea, 2.0 * self.ea, 2.0 * self.ea / 100.0)
        y = []
        for para in x:
            y.append(self.sig_c(para))
        y = np.array(y)
        plt.plot(x, y, 'b-')
        plt.grid()
        plt.show()


class ConcNonlinear:
    def __init__(self, sig_b):
        self.tokg = 10.1972
        self.tosi = 0.0980665
        self.sig_b = sig_b  # (N/mm2)
        self.ft = -1.8 * math.sqrt(self.sig_b * self.tokg) * self.tosi  # Tension Strength N/mm2

        self.ec = 4.0 * (self.sig_b * self.tokg / 1000.0) ** (0.333) * 10 ** 5
        self.ec = self.ec * self.tosi
        self.e0 = 0.5243 * (self.sig_b * self.tokg) ** (0.25) * 10.0 ** (-3)

        self.et = self.ft / self.ec
        self.eu = 10.0 * self.et

        self.alpha = self.ec / self.sig_b * self.e0
        self.c = 1.67 * self.sig_b

    def sig_c(self, e):
        if e <= self.eu:
            return 0.0
        elif self.eu < e and e <= self.et:
            xx = (-e + self.et) / (-self.eu + self.et)
            return self.ft * (1.0 - 8.0 / 3.0 * xx + 3.0 * xx ** 2 - 4.0 / 3.0 * xx ** 3)
        elif self.et < e and e <= 0.0:
            return self.ec * e
        elif 0 < e and e <= self.e0:
            return self.sig_b * (1.0 - (1.0 - e / self.e0) ** (self.alpha))
        elif self.e0 < e:
            s = self.sig_b * math.exp(- self.c * (e - self.e0) ** 1.15)
            if s <= 0.0:
                return 0.0
            return self.sig_b * math.exp(- self.c * (e - self.e0) ** 1.15)
        else:
            print("error sig_c!, e=", e)

    def ecs(self, sig_s):
        return self.e0 * (1.0 - (1.0 - sig_s / self.sig_b) ** (1.0 / self.alpha))

    def ect(self):
        return self.et

    def test(self):
        x = np.arange(self.eu * 1.5, self.e0 * 10, (self.e0 - self.eu * 4) / 100.0)
        y = []
        for para in x:
            y.append(self.sig_c(para))
        y = np.array(y)
        plt.plot(x, y, 'b-')
        plt.grid()
        plt.show()

    def model(self, ax, canv):
        fig = plt.figure()
        x = np.arange(self.eu * 1.5, self.e0 * 4, (self.e0 - self.eu * 4) / 100.0)
        y = []
        for para in x:
            y.append(self.sig_c(para))
        y = np.array(y)
        ax.girid()
        ax.plot(x, y, 'b-')
        canv.draw()

    def image_pdf(self, imagefile):

        fig = plt.figure()
        ax = plt.axes()
        x = np.arange(self.eu * 1.5, self.e0 * 4, (self.e0 - self.eu * 4) / 100.0)
        y = []
        for para in x:
            y.append(self.sig_c(para))
        y = np.array(y)
        ax.plot(x, y, 'b-')
        plt.savefig(imagefile)


class Steel:
    def __init__(self, es, fy):
        if es == -99:
            self.es = 2.05 * 10 ** 5
        else:
            self.es = es
        self.fy = fy
        self.est = self.es
        self.ey = self.fy / self.es
        self.ey2 = self.fy / self.est
        self.es2 = self.es / 100.0

    def sig_s(self, e):

        if e < -self.ey2:
            return -self.fy - self.es2 * (abs(e) - self.ey2)
        elif -self.ey2 <= e and e <= 0.0:
            return self.est * e
        elif 0.0 < e and e <= self.ey:
            return self.es * e
        elif self.ey < e:
            return self.fy + self.es2 * (e - self.ey)

    def st_s(self, sig):
        return sig / self.es

    def test(self):

        x = np.arange(-self.ey * 20.0, self.ey * 20.0, self.ey / 100.0)
        y = []
        for para in x:
            y.append(self.sig_s(para))
        y = np.array(y)
        plt.plot(x, y, 'b-')
        plt.show()


if __name__ == '__main__':
    steel = Steel(-99, 490)
    steel.test()
