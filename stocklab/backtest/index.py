import numpy as np


class Index(object):
    def __init__(self, indexes, col_name):
        assert isinstance(indexes, (list, np.ndarray))
        assert len(indexes) > 0
        self.indexes = iter(indexes)
        self.col_name = col_name
        self.current = None

    def next(self):
        try:
            self.current = self.indexes.__next__()
        except StopIteration:
            self.current = None
        finally:
            return self.current
