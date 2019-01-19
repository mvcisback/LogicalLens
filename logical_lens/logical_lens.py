from itertools import combinations
from typing import Mapping, Sequence, TypeVar

import attr
import funcy as fn
import monotone_bipartition as mbp
import numpy as np


DATA = TypeVar('D')  # Abstract type for input data.
LENS = Mapping[DATA, Mapping[Sequence[float], bool]]


@attr.s(auto_attribs=True, frozen=True)
class LogicalLens:
    n: int = attr.ib()  # TODO: assert n >= 1
    lens: LENS

    def boundary(self, data, *, approx=False, tol=None):
        assert (not approx) or (tol is not None)
        boundary = mbp.from_threshold(self.lens(data), self.n)
        if not approx:
            return boundary
        return boundary.approx(tol=tol)

    def dist(self, data1, data2, tol=1e-3):
        b1, b2 = map(self.boundary, (data1, data2))
        return b1.dist(b2, tol=tol)

    def adj_matrix(self, data):
        n = len(data)
        A = np.zeros((n, n))
        for i, j in combinations(range(n), 2):
            A[i, j] = self.dist(data1, data2)
            A[j, i] = A[i, j]

        return A

    def _projector(self, point_or_order, lexicographic=False, tol=1e-4):
        assert len(point_or_order) == self.n
        return lambda d: self.boundary(d).project(
            point_or_order, tol=tol, lexicographic=lexicographic)

    def _random_projector(self):
        return self.projector(np.random.uniform(0, 1, self.n))

    def projector(self, points, tol=1e-4):
        return fn.ljuxt(*(self._projector(p, tol) for p in points))

    def random_projector(self, n):
        return fn.ljuxt(*(self._random_projector() for _ in range(n)))

    def lex_projectors(self, orders):
        fs = (self._projector(o, tol, lexicographic=True) for o in orders)
        return fn.ljuxt(*fs)
