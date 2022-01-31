import scipy.signal
from maker.utils import Slope,Rel,Range

class Lines:
    def __init__(self, data: list):
        self.d = data
        self.support, self.resistance = self.create()

    def create(self) -> (Slope, Slope):
        raise NotImplemented

    @property
    def relation(self):
        diff = self.resistance.angle - self.support.angle
        rel = Rel.straight
        if diff > 0:
            rel = Rel.diverge
        elif diff < 1:
            rel = Rel.converge
        return rel, diff

    @staticmethod
    def get_slope(points: Range) -> Slope:
        """
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        """
        m = (points.end.value - points.start.value) / (points.end.idx - points.start.idx)
        b = points.start.value - m * points.start.idx
        return Slope(m=m, b=b)

    @property
    def peaks(self):
        upper_peaks = scipy.signal.find_peaks(self.d)
        lower_peaks = scipy.signal.find_peaks([x * -1 for x in self.d])
        if len(upper_peaks) < 1 or len(lower_peaks) < 1:
            return [], []
        return upper_peaks[0], lower_peaks[0]

    def predict(self,new_data,xs=None):
        if xs is None:
            xs = list(range(len(new_data) + len(self.d)))
        upper_limit = [x * self.resistance.m + self.resistance.b for x in xs]
        lower_limit = [x * self.support.m + self.support.b for x in xs]
        return upper_limit, lower_limit
