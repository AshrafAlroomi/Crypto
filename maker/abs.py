import scipy.signal
import math
import matplotlib.pyplot as plt
from maker.utils import Slope, Rel, Range


class Lines:
    def __init__(self, data: list, xs: list = None):
        self.d = data
        if xs is None:
            xs = list(range(len(data)))
        assert len(xs) == len(data)
        self.xs = xs
        self.support, self.resistance = self.create()

    def create(self) -> (Slope, Slope):
        """abstract method"""
        raise NotImplemented

    @property
    def dis(self):
        # parallel lines
        d = abs(self.resistance.b - self.support.b) / math.sqrt(self.resistance.m + 1)
        return d

    @property
    def relation(self):
        """the relation between the support and resistance lines"""
        diff = self.resistance.angle - self.support.angle
        rel = Rel.straight
        if diff > 0:
            rel = Rel.diverge
        elif diff < 1:
            rel = Rel.converge
        return rel, diff

    @staticmethod
    def get_slope(points: Range) -> Slope:
        """ define slope by theta and intercept
        theta = (y2 - y1) / (x2 - x1)
        intercept= y1 - m * x1
        """
        m = (points.end.value - points.start.value) / (points.end.idx - points.start.idx)
        b = points.start.value - m * points.start.idx
        return Slope(m=m, b=b)

    @property
    def peaks(self):
        """get upper and lower peaks of data"""
        upper_peaks = scipy.signal.find_peaks(self.d)
        lower_peaks = scipy.signal.find_peaks([x * -1 for x in self.d])
        if len(upper_peaks) < 1 or len(lower_peaks) < 1:
            return [], []
        return upper_peaks[0], lower_peaks[0]

    def show(self):
        """plot support,resistance and data"""
        plt.plot(self.xs, self.d, label="data")
        r, s = self.predict()
        plt.plot(s, label="support")
        plt.plot(r, label="resistance")
        plt.legend(loc="upper left")
        plt.show()

    def predict(self, length=0, xs=None):
        """create slope prediction of next data
        either length of the prediction line :arg length
        or the data point index :arg xs"""
        if xs is None:
            xs = list(range(length + len(self.d)))
        r = [self.resistance.y(x) for x in xs]
        s = [self.support.y(x) for x in xs]
        return r, s
