import math
import openpyxl
from openpyxl.utils import get_column_letter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas
import os


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

