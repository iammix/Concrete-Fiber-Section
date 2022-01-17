import numpy as np


class Aij():
    def Ec(self, fc: float, gamma: float) -> float:
        return 3.35 * 10 ** 4 * (gamma / 24.0) ** (2) * (fc / 60.0) ** (1.0 / 3.0)

    def rebar_area(self, index: str) -> float:
        try:
            dia = float(index[1:])
            return (np.pi * dia ** 2) / 4
        except:
            raise ValueError

    def diameter(self, index: str) -> int:
        """Return diameter given the string"""
        try:
            return int(index[1:])
        except:
            raise ValueError


if __name__ == '__main__':
    obj = Aij()
    print(obj.rebar_area("d10"))
