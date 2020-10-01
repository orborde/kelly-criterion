#! /usr/bin/env python3

import enum
import itertools
import math
import numpy
from typing import *

import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def utility_log_log(W):
    return math.log(math.log(W+1)+1)

def utility_log(W):
    return math.log(W)

P_win = 1/2
B = 2
N = 11

kelly_fraction = P_win - (1-P_win) / B
print('kelly fraction:', kelly_fraction)

class Outcome(enum.Enum):
    W = "W"
    L = "L"

def single_round(initial_wealth, f, outcome: Outcome):
    wager = f * initial_wealth
    if outcome == Outcome.W:
        winnings = wager * (B+1)
    else:
        winnings = 0

    return (
        initial_wealth
        -
        wager
        +
        winnings
    )

def final_wealth(initial_wealth, f, outcomes: List[Outcome]):
    wealth = initial_wealth
    for outcome in outcomes:
        wealth = single_round(wealth, f, outcome)
    return wealth

def final_wealth_by_ct(initial_wealth, f, wins, losses):
    p = (P_win ** wins) * ((1 - P_win)**losses) * nCr(wins, (wins+losses))
    outcomes = [Outcome.W]*wins + [Outcome.L]*losses
    return p, outcomes

def p(outcomes: List[Outcome]):
    wins = outcomes.count(Outcome.W)
    losses = outcomes.count(Outcome.L)
    return (P_win ** wins) * ((1 - P_win) ** losses)


def expected_utility(f, utility, n):
    possible_worlds = [
        (p(outcomes), final_wealth(1, f, outcomes))
        for outcomes in itertools.product(Outcome, repeat=n)
    ]

    return sum(utility(wealth)*p for p,wealth in possible_worlds)

import matplotlib.pyplot as pyplot

fs = numpy.linspace(0,1,100)
fs = fs[:-1]
for n in range(N):
    pyplot.plot(fs, [expected_utility(f, utility_log, n) for f in fs], label=str(n))
pyplot.axvline(x=kelly_fraction)
pyplot.legend()
pyplot.show()