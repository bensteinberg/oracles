from itertools import product
from pytest import raises
from hypothesis import given
import hypothesis.strategies as st


# property-based tests
# 6d6
@given(st.lists(st.integers(1, 6), min_size=6, max_size=6))
def test_oracle(roll):
    from oracles.main import Oracle, oracles
    for o in oracles:
        bp = Oracle(o['name'], roll)
        assert bp.oracle == o['name']
        assert bp.text != ''


# 6dwhatever
@given(st.lists(st.integers(1), min_size=6, max_size=6))
def test_oracle_bad_dice(roll):
    from oracles.main import Oracle, oracles
    for o in oracles:
        if any(map(lambda a: a > 6, roll)):
            with raises(ValueError):
                bp = Oracle(o['name'], roll)
        else:
            bp = Oracle(o['name'], roll)
            assert bp.oracle == o['name']
            assert bp.text != ''


# enumerate all rolls
# 6d6
def test_oracles():
    from oracles.main import Oracle, oracles
    # there are 46,656 unique rolls of six six-sided dice
    rolls = [list(map(lambda a: a + 1, list(p)))
             for p in product(range(6), repeat=6)]

    os = []
    for o in oracles:
        for r in rolls:
            os.append(Oracle(o['name'], r))

    # confirm all possible oracles were created
    assert len(os) == 46656 * len(oracles)

    # confirm all oracles are unique
    texts = ['%s%s' % (o.oracle, o.text) for o in os]
    assert len(texts) == len(set(texts))


# 6d7
def test_bad_rolls():
    from oracles.main import Oracle, oracles
    # there are 117,649 unique rolls of six seven-sided dice,
    # and 70,993 of them contain at least one seven:
    # sum([7 in r for r in bad_rolls])
    bad_rolls = [list(map(lambda a: a + 1, list(p)))
                 for p in product(range(7), repeat=6)]
    os = []
    for o in oracles:
        for r in bad_rolls:
            if 7 in r:
                with raises(ValueError):
                    os.append(Oracle(o['name'], r))
            else:
                os.append(Oracle(o['name'], r))
    assert len(os) == (117649 - 70993) * len(oracles)
