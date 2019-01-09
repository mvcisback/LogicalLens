# LogicalLens

## Proposed API
```python
from logical_lens import LogicalLens

p1 = (0.1, 0.1)  # Point in [0, 1]^2
p2 = (0.2, 0.3)  # Point in [0, 1]^2

x1 = .. # some arbitrary data object.
x2 = ..

# Define some logical lens. TODO
f = ..  # Data -> (Point -> bool)
lens = LogicalLens(lens=f)  # Wrapper around logical lens to add functionality.
                            # Is still callable, e.g., lens(x1) == f(x1)

# Note: forall all data, x, lens(x) must be a monotone threshold function.
assert lens(x1)(p1) <= lens(x1)(p2)  # Recall that False <= True


# Compute Logical Distances.
d = lens.dist(x1, x2)
A = lens.adj_matrix(data=[x1, x2, x3, x4])

# Find points on boundaries for coarse estimates.

Y = lens.project(
    indices=[(0, 1), (1, 0.3)],  # points on hyperfaces of hypercube not connected to the origin.
                                 # Resulting lines intersects the boundary of the hyperbox at the 
                                 # origin and at the indicies.
                                 # Will raise exception if point on boundary is not valid.
    data=[x1, x2],  # Iterable of data
    as_percent=True  # Return number between 0 and 1 giving where on linear interpolation 
                     # between 0 and index intersection occurs. If false, give point on line.
                     # Default is true
)

Y2 = lens.random_project(data=[x1, x2], n=10)  # Project onto 10 random lines.
```
