import argparse
import random
from data import oracles

# check completeness of data
# (we test that we can generate all possible seeds in test_oracles.py)
assert all(map(lambda a: a == 6, [len(o['trends']) for o in oracles]))
assert all(map(lambda a: a == 6, [len(o['impacts']) for o in oracles]))
element_counts = [[len(e) for e in o['elements']] for o in oracles]
flattened_element_counts = [y for x in element_counts for y in x]
assert all(map(lambda a: a == 8, flattened_element_counts))
assert len(flattened_element_counts) == 6 * len(oracles)

choices = [o['name'] for o in oracles]


class OracleAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        super(OracleAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """
        This is redundant with Oracle's __init__ for cleanliness of
        error messages...
        """
        found = [values in choice for choice in choices]
        if sum(found) == 1:
            setattr(namespace,
                    self.dest,
                    choices[[i for i, x in enumerate(found) if x][0]])
            return
        elif sum(found) == 0:
            qualifier = "not a valid"
        else:
            qualifier = "an ambiguous"
        raise argparse.ArgumentError(self,
                                     "'%s' is %s choice; "
                                     "try one of %s (or a substring)" %
                                     (values, qualifier, choices))


class Oracle:
    def __init__(self, oracle, dice=None):
        found = [oracle in choice for choice in choices]
        if sum(found) == 1:
            self.oracle = choices[[i for i, x in enumerate(found) if x][0]]
        elif sum(found) == 0:
            qualifier = "not a valid"
        else:
            qualifier = "an ambiguous"
        if sum(found) != 1:
            raise ValueError("'%s' is %s choice" % (oracle, qualifier))

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
        self.element_b = oracles[i]['elements'][c[4]][c[5] + 2]

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('oracle',
                        action=OracleAction,
                        help='use one of the following, or a substring: %s' %
                        choices)
    parser.add_argument('-d', '--dice',
                        nargs=6,
                        type=int,
                        choices=range(1, 7),
                        help='set six coefficients, in the range 1-6')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='show oracle structure')

    args = parser.parse_args()

    if args.dice:
        o = Oracle(args.oracle, args.dice)
    else:
        o = Oracle(args.oracle)

    if args.verbose:
        print(repr(o))
    else:
        print(o)


if __name__ == '__main__':
    main()
