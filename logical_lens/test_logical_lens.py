from logical_lens import LogicalLens


def line_lens(a):
    return lambda x: x[0] + x[1] >= a


def test_boundary():
    lens = LogicalLens(2, line_lens)
    b = lens.boundary(0.5)
    assert b.label((0.6, 0.6))
    assert not b.label((0.1, 0.1))


def test_boundary_approx():
    lens = LogicalLens(2, line_lens)
    recs = lens.boundary(0, approx=True, tol=1e-3)
    assert len(recs) == 1


def test_dist():
    lens = LogicalLens(2, line_lens)
    d = lens.dist(0, 0.5).center
    assert abs(d - 0.5) <= 1e-3


def test_adj_matrix():
    lens = LogicalLens(2, line_lens)
    A = lens.adj_matrix([0, 0, 0.1, 0.2])
    assert A.max() < 0.3


def test_projector():
    lens = LogicalLens(2, line_lens)
    f = lens.projector([(0.5, 0.5), (1, 0)])
    x, y = f(0.5)
    assert abs(x - 0.25) < 1e-3
    assert abs(y - 0.5) < 1e-3


def test_rand_projector_smoke():
    lens = LogicalLens(2, line_lens)
    f = lens.random_projector(3)
    assert len(f(0.5)) == 3


def test_lex_projector():
    lens = LogicalLens(2, line_lens)
    f = lens.lex_projector([
        [(0, False), (1, False)],
        [(0, True), (1, True)],
    ])
    x = f(0.5)
    assert len(x) == 2
    assert abs(x[0][0] - 0.5) < 1e-3
    assert abs(x[0][1]) < 1e-3
