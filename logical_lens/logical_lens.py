from itertools import combinations
from typing import Mapping, Sequence, TypeVar
from pathos.multiprocessing import ProcessingPool as Pool

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
            A[i, j] = self.dist(data[i], data[j]).center
            A[j, i] = A[i, j]

        return A

    def _projector(self, point_or_order, *,
                   lexicographic=False, tol=1e-4, percent=True):
        assert len(point_or_order) == self.n
        if lexicographic:
            percent = False

        def project(d):
            res = self.boundary(d).project(
                point_or_order, tol=tol,
                lexicographic=lexicographic, percent=percent
            )
            return res.center if lexicographic else res

        return project


    def _parallel_projector(self, point_or_order, *,
                   lexicographic=False, tol=1e-4, percent=True):
        projector = self._projector(point_or_order, lexicographic=lexicographic,
                                    tol=tol, percent=percent)
        def parallel_project(d):
            with Pool() as pool:
                return pool.map(projector, d)

        return parallel_project


    def _random_projector(self):
        xs = np.random.uniform(0, 1, self.n)
        ys = np.random.uniform(0, 1, self.n)
        return self.projector(tuple(zip(xs, ys)))

    def projector(self, points, tol=1e-4):
        return fn.ljuxt(*(self._projector(p, tol=tol) for p in points))

    def parallel_projector(self, points, tol=1e-4):
        return fn.ljuxt(*(self._parallel_projector(p, tol=tol) for p in points))

    def random_projector(self, n):
        return fn.ljuxt(*(self._random_projector() for _ in range(n)))

    def lex_projector(self, orders, tol=1e-4):
        fs = (self._projector(o, tol=tol, lexicographic=True) for o in orders)
        return fn.ljuxt(*fs)
