# LogicalLens

A "logical lens" is a map: `f : Data -> ([0, 1]^n -> bool)` and is
interpreted as a family of properties over the hyper unit box, `[0,
1]^n`, indexed by "`Data`". Further, `f` must be monotonic threshold
function. That is, given a fixed data `data`, the map `g = f(data)` is
such that for any two points in the unit box, `x, y in [0, 1]^n` if `x
<= y` coordinate-wise, then `g(x) <= g(y)` , where `False <= True`. An
example is given below (see
[monotone-bipartition](https://github.com/mvcisback/monotone-bipartition)
for details):

<figure>
  <img src="assets/bipartition.svg" alt="mbp logo" width=300px>
</figure>

In principle, `Data` can be anything from time-series to pictures of
dogs. The key idea is that a logical lens using embedding
domain specific knowledge in the form of property tests
to design features and similarity measures.

For details on this formalism, see the following two papers:

1. [Vazquez-Chanlatte, Marcell, et al."Time Series Learning using Monotonic Logical Properties.", International Conference on Runtime Verification, RV, 2018](https://mjvc.me/papers/rv2018_logical_ts_learning.pdf)

1. [Vazquez-Chanlatte, Marcell, et al. "Logical Clustering and Learning for Time-Series Data." International Conference on Computer Aided Verification. Springer, Cham, 2017.](https://mjvc.me/papers/cav2017.pdf)

In this readme, for demonstration purposes, we will be using the
`metric-temporal-logic` package. This package provides parametric
properties over time-series and can be installed with:

> $ pip install metric-temporal-logic

```python
from logical_lens import LogicalLens

x1 = .. # some arbitrary data object.
x2 = ..

# Define some logical lens. TODO
f = ..  # Data -> (Point -> bool)
lens = LogicalLens(lens=f)  # Wrapper around logical lens to add functionality.
                            # Is still callable, e.g., lens(x1) == f(x1)

p1 = (0.1, 0.1)  # Point in [0, 1]^2
p2 = (0.2, 0.3)  # Point in [0, 1]^2


# Note: forall all data, x, lens(x) must be a monotone threshold function.
assert lens(x1)(p1) <= lens(x1)(p2)  # Where in python, False <= True.


# Compute Logical Distances.
d = lens.dist(x1, x2)
A = lens.adj_matrix(data=[x1, x2, x3, x4])

# Find points on boundaries for coarse estimates.

## Find intersection of threshold surface and
## the lines intersecting the origin and the points
## provided.
f = lens.projector([(0, 1), (1, 0.3)])
Y = map(f, [x1, x2])

## Project onto 10 random lines.
f2 = lens.random_projector(10)

## Project using lexicographic ordering of parameters:
f3 = lens.lex_projector(orders=[
   [(1, False), (0, True)],  # minimizing on axis 1 then maximizing on axis 0.
   [(0, False), (1, False)],  # minimizing on axis 0 then minimizing on axis 1.
])

```

TODO: rewrite for LogicalLens:
Example notebook used in RV2018 submission: https://gist.github.com/mvcisback/e339530f90a380ad1b36ed4e2291c988
