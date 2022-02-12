import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from scipy import stats
from maker.abs import Lines
from maker.utils import Slope, Point, Range


# class UniLines(Lines):
#     def create(self):
#         upper, lower = self.get_points
#         self.support = self.get_slope(lower)
#         self.resistance = self.get_slope(upper)
#
#     @property
#     def get_points(self, method="last") -> (Range, Range):
#         if method == "data":
#             ulist = self.d.copy()
#             llist = self.d.copy()
#             max_idx1 = np.argmax(ulist)
#             ulist[max_idx1] = 0
#             max_idx2 = np.argmax(ulist)
#             min_idx1 = np.argmin(llist)
#             llist[min_idx1] = np.inf
#             min_idx2 = np.argmin(llist)
#         elif method == "peaks":
#             u, l = self.peaks
#             ulist = [self.d[x] if x in u else 0 for x in range(len(self.d))]
#             llist = [self.d[x] if x in l else np.inf for x in range(len(self.d))]
#
#             max_idx1 = np.argmax(ulist)
#             ulist[max_idx1] = 0
#             max_idx2 = np.argmax(ulist)
#             min_idx1 = np.argmin(llist)
#             llist[min_idx1] = np.inf
#             min_idx2 = np.argmin(llist)
#         else:
#             u, l = self.peaks
#             max_idx1 = u[0]
#             max_idx2 = u[-1]
#             min_idx1 = l[0]
#             min_idx2 = l[-1]
#
#         upper = Range(start=Point(idx=max_idx2, value=self.d[max_idx2]),
#                       end=Point(idx=max_idx1, value=self.d[max_idx1]))
#
#         lower = Range(start=Point(idx=min_idx1, value=self.d[min_idx1]),
#                       end=Point(idx=min_idx2, value=self.d[min_idx2]))
#
#         return upper, lower

class PeaksLines(Lines):
    """draw lines based on data peaks , the angle based on the linear regression of upper and
    lower peaks , the make the lines touch the max and the min of data
    """

    def create(self):
        u, d = self.peaks  # get upper and lower peaks
        ulist = [self.d[x] for x in u]  # get ys of upper peaks
        dlist = [self.d[x] for x in d]  # get ys of lower peaks
        uline = stats.linregress(y=ulist, x=[self.xs[x] for x in u])  # create upper linear regression
        dline = stats.linregress(y=dlist, x=[self.xs[x] for x in d])  # create lower linear regression
        # get min and max
        max_idx = np.argmax(self.d)
        min_idx = np.argmin(self.d)
        max_value = self.d[max_idx]
        min_value = self.d[min_idx]
        # get predictions
        pre_max = uline.slope * self.xs[max_idx] + uline.intercept
        pre_min = dline.slope * self.xs[max_idx] + dline.intercept
        # the difference between predicted and the actual
        diff_max = max_value - pre_max
        diff_min = pre_min - min_value
        # create the lines
        support = Slope(m=dline.slope, b=dline.intercept - diff_min)
        resistance = Slope(m=uline.slope, b=uline.intercept + diff_max)
        return support, resistance


class StraightLines(Lines):
    """draw Straight lines based on max min value of the data
    """

    def create(self):
        max_value = np.max(self.d)
        min_value = np.min(self.d)
        support = Slope(m=0.0, b=min_value)
        resistance = Slope(m=0.0, b=max_value)
        return support, resistance


class ParLines(Lines):
    """draw parallel lines based on the linear regression of the data
    make the lines touch the min and max of data
    """

    def create(self):
        l = stats.linregress(y=self.d, x=self.xs)  # create liner regression
        # get min and max
        max_idx = np.argmax(self.d)
        min_idx = np.argmin(self.d)
        max_value = self.d[max_idx]
        min_value = self.d[min_idx]
        # get predictions
        pre_max = l.slope * self.xs[max_idx] + l.intercept
        pre_min = l.slope * self.xs[min_idx] + l.intercept
        # the difference between predicted and the actual
        diff_max = max_value - pre_max
        diff_min = pre_min - min_value
        # create the lines
        support = Slope(m=l.slope, b=l.intercept - diff_min)
        resistance = Slope(m=l.slope, b=l.intercept + diff_max)
        return support, resistance


@dataclass
class LinesTester:
    """make predictions and test support,resistance lines"""
    lines: Lines

    def __post_init__(self):
        # create lines data
        self.support_data = [self.lines.support.y(i) for i in self.lines.xs]
        self.resistance_data = [self.lines.resistance.y(i) for i in self.lines.xs]

    def score(self):
        # TODO
        """get score how much efficient the lines"""
        up_peaks, down_peaks = self.lines.peaks
        up_diff = down_diff = 0
        if len(up_peaks) > 1 and len(down_peaks) > 1:
            for i in up_peaks:
                up_diff += abs(self.lines.d[i] - self.resistance_data[i])
            for i in down_peaks:
                down_diff += abs(self.lines.d[i] - self.support_data[i])
        return self.lines.relation, up_diff, down_diff

    def test(self, data, xs=None):
        """create new data predictions and plot"""
        if xs is None:
            last_idx = self.lines.xs[-1]
            xs = [x + last_idx for x in range(len(data))]
        plt.plot(self.lines.xs, self.lines.d, label="data")
        plt.plot(self.lines.xs, self.support_data, label="support")
        plt.plot(self.lines.xs, self.resistance_data, label="resistance")
        plt.plot(xs, data, label="pre")
        plt.legend(loc="upper left")
        plt.show()

    def show(self):
        """plot support,resistance and data"""
        plt.plot(self.lines.xs, self.lines.d, label="data")
        plt.plot(self.lines.xs, self.support_data, label="support")
        plt.plot(self.lines.xs, self.resistance_data, label="resistance")
        plt.legend(loc="upper left")
        plt.show()

    # def __outlier(self):
    #     self.support_outlier_count = 0
    #     self.resistance_outlier_count = 0
    #     s_avg = 0.0
    #     r_avg = 0.0
    #     data_mean = np.mean(self.lines.d)
    #     for i in range(len(self.lines.d)):
    #         if self.resistance_data[i] < self.lines.d[i]:
    #             self.resistance_outlier_count += 1
    #             r_avg += data_mean - self.resistance_data[i]
    #         if self.support_data[i] > self.lines.d[i]:
    #             self.support_outlier_count += 1
    #             s_avg += self.support_data[i] - data_mean
    #     print(r_avg)
    #     print(s_avg)
