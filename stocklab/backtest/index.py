import datetime

import numpy as np
from dataclasses import dataclass
from typing import Union


@dataclass
class Index(object):
    indexes: Union[list, np.ndarray, iter]
    col_name: str
    current = None

    def __post_init__(self):
        self.row = self.indexes
        self.indexes = iter(self.indexes)

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
