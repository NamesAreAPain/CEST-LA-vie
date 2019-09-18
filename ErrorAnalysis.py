import csv
import math
import numpy as np
import re
import sys
from math import sqrt

sys_error_presets = {
    "10kOhm": "0.0090*0.01*self.value + 0.0006 * 0.01 * 10",
    "1kOhm": "0.0090*0.01*self.value + 0.0006 * 0.01 * 1",
    "10V": "0.0030*0.01*self.value + 0.0005 * 0.01 * 10",
    "1V": "0.0030*0.01*self.value + 0.0006 * 0.01 * 1",
    "100V": "0.0050*0.01*self.value + 0.0006 * 0.01 * 100",
    "Exact": "0"
}


def dist(x, y):
    return sqrt(x ** 2 + y ** 2)


class DataPoint:
    def __init__(self, values, sys_error_eq, val=0, err=0, override=False):
        if not override:
            values = list(map(float, values))
            self.value = np.mean(values)
            if len(values) > 1:
                self.rng_error = np.std(values, ddof=1) / np.sqrt(abs(self.value))
            else:
                self.rng_error = 0
            exec("self.sys_error = " + sys_error_eq)
            self.error = sqrt(self.rng_error ** 2 + self.sys_error ** 2)
        else:
            self.value = val
            self.error = err

    def __add__(self, other):
        return DataPoint(0, 0, override=True, val=self.value + other.value, err=dist(self.error, other.error))

    def __mul__(self, other):
        if isinstance(other, DataPoint):
            return DataPoint(0, 0, override=True, val=self.value * other.value,
                             err=abs(self.value * other.value) * sqrt(
                                 (self.error / self.value) ** 2 + (other.error / other.value) ** 2))
        else:
            return DataPoint(0, 0, override=True, val=self.value * other, err=self.error * abs(other))

    def __truediv__(self, other):
        if isinstance(other, DataPoint):
            ERR = lambda a, b: abs(a.value / b.value) * sqrt((a.error / a.value) ** 2 + (b.error / b.value) ** 2)
            return DataPoint(0, 0, override=True, val=self.value / other.value, err=ERR(self, other))
        else:
            return self.__mul__(self, 1 / other)

    def __sub__(self, other):
        return self.__add__(other * -1)

    def __pow__(self, other):
        ERR = lambda a, b: abs(a.value ** b) * abs(b) * self.error / abs(self.value)
        return DataPoint(0, 0, override=True, val=self.value ** other, err=ERR(self, other))

    def __repr__(self):
        return "" + str(self.value) + "±" + str(self.error)


def ErrAnaFormatter(filename):
    with open(filename, 'r', newline='') as csvIn, open(filename[:-4] + "ErrAna.csv", 'w', newline='') as csvOut:
        reader = csv.DictReader(csvIn)
        writer_fieldnames = []
        errana_names = {}
        nonfig_names = []
        calc_names = {}
        for fname in reader.fieldnames:
            if len(fname) >= 4 and fname[-3:] == "_T1":
                errana_names[fname[:-3]] = 0
                writer_fieldnames.append(fname[0:-3] + "_BST")
                writer_fieldnames.append(fname[0:-3] + "_ERR")
            elif len(fname) >= 4 and bool(re.match("_T\d+", fname[-3:])):
                errana_names[fname[:-3]] = errana_names[fname[:-3]] + 1
            elif len(fname) >= 5 and fname[:5] == "CALC_":
                calc_names[fname[5:]] = "UNSET"
                writer_fieldnames.append(fname[5:] + "_BST")
                writer_fieldnames.append(fname[5:] + "_ERR")
            else:
                nonfig_names.append(fname)
                writer_fieldnames.append(fname)
        writer = csv.DictWriter(csvOut, fieldnames=writer_fieldnames)
        writer.writeheader()
        sys_error_dict = {}
        print(sys_error_presets)
        for row in reader:
            rowout = {}
            vardict = {}
            for col in nonfig_names:
                rowout[col] = row[col]
            for fname, count in errana_names.items():
                values = []
                for col in [fname + "_T" + str(n) for n in range(1, count + 2)]:
                    values.append(row[col])
                if not fname in sys_error_dict:
                    print("SYSTEMATIC ERROR FOR " + fname)
                    sys_error_dict[fname] = sys_error_presets[input()]
                vardict[fname] = DataPoint(values, sys_error_dict[fname])
                rowout[fname + "_BST"] = vardict[fname].value
                rowout[fname + "_ERR"] = vardict[fname].error
            for col in calc_names:
                if row["CALC_" + col] != "" and calc_names[col] == "UNSET":
                    brokenIn = (row["CALC_" + col]).split(" ")
                    brokenOut = ""
                    for word in brokenIn:
                        if word in vardict:
                            brokenOut += "vardict['" + word + "'] "
                        else:
                            brokenOut += word + " "
                    calc_names[col] = brokenOut
                VAR = eval(str(calc_names[col]))
                vardict[col] = VAR
                rowout[col + "_BST"] = VAR.value
                rowout[col + "_ERR"] = VAR.error
            writer.writerow(rowout)
        return csvOut.name


if __name__ == "__main__":
    ErrAnaFormatter(sys.argv[1])
