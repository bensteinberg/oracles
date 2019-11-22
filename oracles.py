import click
import random
import importlib
import os

data_source = os.environ.get('ORACLES') or 'data'
oracles = importlib.import_module(data_source).oracles

# check completeness of data
# (we test that we can generate all possible seeds in test_oracles.py)
assert all(map(lambda a: a == 6, [len(o['trends']) for o in oracles]))
assert all(map(lambda a: a == 6, [len(o['impacts']) for o in oracles]))
element_counts = [[len(e) for e in o['elements']] for o in oracles]
flattened_element_counts = [y for x in element_counts for y in x]
assert all(map(lambda a: a == 6, flattened_element_counts))
assert len(flattened_element_counts) == 8 * len(oracles)

choices = [o['name'] for o in oracles]


def validate_oracle(value):
    found = [value in choice for choice in choices]
    if sum(found) == 1:
        return (choices[[i for i, x in enumerate(found) if x][0]], None)
    elif sum(found) == 0:
        qualifier = "not a valid"
    else:
        qualifier = "an ambiguous"
    return(None, qualifier)


def validate_oracle_option(ctx, param, value):
    if not value:
        return
    (o, qualifier) = validate_oracle(value)
    if qualifier:
        raise click.BadParameter("'%s' is %s choice" % (value, qualifier))
    else:
        return o


class Oracle:
    def __init__(self, oracle, dice=None):
        (o, qualifier) = validate_oracle(oracle)
        if qualifier:
            raise ValueError("'%s' is %s choice" % (oracle, qualifier))
        else:
            self.oracle = o

        if dice:
            if all(map(lambda a: a in range(1, 7), dice)) and len(dice) == 6:
                self.dice = dice
            else:
                raise ValueError('You must use 6d6.')
        else:
            self.dice = [random.choice(range(0, 6)) + 1 for _ in range(0, 6)]

        # change dice rolls to zero-based for list indexing
        c = [n for n in map(lambda a: a - 1, self.dice)]
        i = choices.index(self.oracle)

        self.trend = oracles[i]['trends'][c[0]]
        self.element_a = oracles[i]['elements'][c[1]][c[2]]
        self.impact = oracles[i]['impacts'][c[3]]
        # the last roll needs an offset
        self.element_b = oracles[i]['elements'][c[4] + 2][c[5]]

        self.text = "%s %s %s %s" % (self.trend,
                                     self.element_a,
                                     self.impact,
                                     self.element_b)

        # we expose the reversal since it can't necessarily
        # be produced by a transformation of the dice
        self.reversal = "%s %s %s %s" % (self.trend,
                                         self.element_b,
                                         self.impact,
                                         self.element_a)

    def __str__(self):
        return self.text

    def __repr__(self):
        return "<Oracle '%s' %s '%s'>" % (self.oracle, self.dice, self.text)


@click.command()
@click.option('-o', '--oracle',
              callback=validate_oracle_option,
              help='use one of the following, or a substring: %s' % choices)
@click.option('-d', '--dice',
              nargs=6, type=click.IntRange(1, 6),
              help='roll 6d6')
@click.option('-v', '--verbose',
              is_flag=True,
              help='show oracle structure')
def main(oracle, dice, verbose):

    """This is a program for generating Big Pictures for Ben Robbins'
    excellent game, Microscope, using the Oracles mechanism from
    Microscope Explorer.

    See http://www.lamemage.com/microscope/ for more.

    """

    if not oracle:
        oracle = random.choice(choices)

    if dice:
        o = Oracle(oracle, dice)
    else:
        o = Oracle(oracle)

    if verbose:
        print(repr(o))
    else:
        print(o)
