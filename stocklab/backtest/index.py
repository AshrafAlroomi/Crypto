import datetime

import numpy as np


class Index(object):
    def __init__(self, indexes, col_name):
        assert isinstance(indexes, (list, np.ndarray))
        assert len(indexes) > 0
        self.row = indexes
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

    def get_index(self, value):
        return self.row.index(value)

    def get_period(self, start_index, end_index):
        return self.row[start_index, end_index]


