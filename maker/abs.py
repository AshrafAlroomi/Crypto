import scipy.signal
from maker.utils import Slope, Rel, Range


class Lines:
    def __init__(self, data: list):
        self.d = data
        self.support, self.resistance = self.create()

    def create(self) -> (Slope, Slope):
        """abstract method"""
        raise NotImplemented

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

    def predict(self, length=0, xs=None):
        """create slope prediction of next data
        either length of the prediction line :arg length
        or the data point index :arg xs"""
        if xs is None:
            xs = list(range(length + len(self.d)))
        r = [self.resistance.y(x) for x in xs]
        s = [self.support.y(x) for x in xs]
        return r, s
