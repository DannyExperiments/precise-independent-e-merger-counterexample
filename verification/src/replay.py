#!/usr/bin/env python3
"""Exact arithmetic checks of both cutoffs, product laws, and witness bounds."""
from fractions import Fraction as Q
from itertools import permutations, product
from math import prod

LOW = Q(1, 4)
HIGH = Q(3, 4)
POINTS = ((LOW, LOW, LOW), (0, LOW, HIGH), (HIGH, 0, LOW), (LOW, HIGH, 0))


def hard(x):
    return int(x > Q(1, 2))


def ramp(x):
    return min(1, max(0, 2 * x - Q(1, 2)))


def weights(bits):
    a, b, c = bits
    return ((1 - b) * c, (1 - c) * a, (1 - a) * b)


def merger(point, cutoff):
    return 1 + sum((x - 1) * w for x, w in zip(point, weights(map(cutoff, point))))


def expectation(laws, cutoff):
    result = Q(0)
    for atoms in product(*laws):
        point, probabilities = zip(*atoms)
        result += merger(point, cutoff) * prod(probabilities)
    return result


def main():
    boolean_outputs = (
        (0, 0, 0), (1, 0, 0), (0, 0, 1), (0, 0, 1),
        (0, 1, 0), (1, 0, 0), (0, 1, 0), (0, 0, 0),
    )
    for bits, intended in zip(product((0, 1), repeat=3), boolean_outputs):
        assert weights(bits) == intended and sum(intended) <= 1
    for a in product((Q(0), LOW, Q(1, 2), HIGH, Q(1)), repeat=3):
        assert sum(weights(a)) == 1 - prod(a) - prod(1 - x for x in a)
        assert sum(weights(a)) <= 1

    full_laws = (
        ((0, Q(2, 3)), (3, Q(1, 3))),
        ((LOW, Q(1, 2)), (Q(7, 4), Q(1, 2))),
        ((1, Q(1)),),
    )
    deficient_law = ((0, Q(1, 2)), (1, Q(1, 2)))
    for cutoff in (hard, ramp):
        values = tuple(merger(point, cutoff) for point in POINTS)
        assert values == (1, 0, 0, 0)
        for i, point in enumerate(POINTS[1:]):
            assert weights(map(cutoff, point))[i] == 1 and point[i] == 0
        assert merger((0, LOW, LOW), cutoff) > merger((0, LOW, HIGH), cutoff)
        for laws in product(full_laws, repeat=3):
            assert expectation(laws, cutoff) == 1
        for laws in product(full_laws + (deficient_law,), repeat=3):
            means = tuple(sum(value * probability for value, probability in law) for law in laws)
            avg_weights = [Q(0)] * 3
            for atoms in product(*laws):
                point, probabilities = zip(*atoms)
                for i, weight in enumerate(weights(map(cutoff, point))):
                    avg_weights[i] += prod(probabilities) * weight
            factored = 1 + sum((mean - 1) * weight for mean, weight in zip(means, avg_weights))
            assert expectation(laws, cutoff) == factored <= 1
        print(f"{cutoff.__name__}: A, B1, B2, B3 = {values}; 27 precise and 64 valid product-law checks")

    # For each first index, check the two possible remaining read orders.
    # Allow those orders and later fractions to depend on which point is seen.
    capital_grid = [Q(i, 4) for i in range(5)]
    all_small = POINTS[0]
    for first in range(3):
        remaining = [i for i in range(3) if i != first]
        zero_point = POINTS[first + 1]
        assert prod(zero_point[i] for i in remaining) == Q(3, 16)
        for c, t in product(capital_grid, repeat=2):
            small_cap = c * (1 - t + t * all_small[first])
            minimum = c * (1 - t) * Q(3, 16)
            assert small_cap <= Q(1, 4) + 4 * minimum
            for order in permutations(remaining):
                for later in product(capital_grid, repeat=2):
                    wealth = c * (1 - t) * prod(1 - u + u * zero_point[i] for u, i in zip(later, order))
                    assert wealth >= minimum
    delta = Q(3, 52)
    assert 1 - delta == LOW + 12 * delta
    print("Lugano truth table, 125 fractional weight triples, and exact gap arithmetic passed")
    print(f"M(A) <= 1/4 + 4 Σ M(B_i); four-point maximum error >= {delta}")


if __name__ == "__main__":
    main()
