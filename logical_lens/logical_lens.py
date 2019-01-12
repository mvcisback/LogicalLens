from typing import Mapping, Sequence, TypeVar

import attr


DATA = TypeVar('D')  # Abstract type for input data.
LENS = Mapping[DATA, Mapping[Sequence[float], bool]]


@attr.s(auto_attribs=True, frozen=True)
class LogicalLens:
    n: int = attr.ib()  # TODO: assert n >= 1
    lens: LENS

    def dist(self, data1, data2):
        raise NotImplementedError

    def adj_matrix(self, data):
        raise NotImplementedError

    def project(self, indices, data, *, as_percent=True):
        raise NotImplementedError

    def random_project(data, n):
        raise NotImplementedError
