from abc import ABC, abstractmethod

import numpy as np


class Index(object):
    def __init__(self, indexes):
        assert isinstance(indexes, (list, np.ndarray))
        assert len(indexes) > 0
        self.indexes = iter(indexes)
        self.current = self.next()

    def next(self):
        try:
            self.current = self.indexes.__next__()
        except StopIteration:
            self.current = False
        finally:
            return self.current
