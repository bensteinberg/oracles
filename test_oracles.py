from oracles import Oracle, oracles
from itertools import product
from pytest import raises


def test_oracles():
    # there are 46,656 unique rolls of six six-sided dice
    rolls = [[d for d in map(lambda a: a + 1, list(p))]
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


def test_bad_rolls():
    # there are 117,649 unique rolls of six seven-sided dice,
    # and 70,993 of them contain at least one seven:
    # sum([7 in r for r in bad_rolls])
    #
    # Try this with QuickCheck?
    bad_rolls = [[d for d in map(lambda a: a + 1, list(p))]
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
