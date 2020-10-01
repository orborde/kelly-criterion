#! /usr/bin/env python3

import enum
import itertools
import math
import numpy
from fractions import Fraction as F
from typing import *
from tqdm import tqdm

import pprint

import operator as op
from functools import reduce

def nCr(n, r):
    assert n > 0
    assert r <= n, (r,n)
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

def utility_log_log(W):
    return math.log(math.log(W+1)+1)

def utility_log(W):
    return math.log(W)

P_win = F(1,2)
B = 2
N = 100

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
    p = (P_win ** wins) * ((1 - P_win)**losses) * nCr((wins+losses), wins)
    outcomes = [Outcome.W]*wins + [Outcome.L]*losses
    return p, final_wealth(initial_wealth, f, outcomes)

def p(outcomes: List[Outcome]):
    wins = outcomes.count(Outcome.W)
    losses = outcomes.count(Outcome.L)
    return (P_win ** wins) * ((1 - P_win) ** losses)


def expected_utility(f, utility, n):
    possible_worlds = [
        final_wealth_by_ct(1, f, wins, (n - wins))
        for wins in range(0, n+1)
    ]

    return sum(utility(wealth)*p for p,wealth in possible_worlds)

import matplotlib.pyplot as pyplot

PREC=10
fs = [kelly_fraction + F(x, PREC)*F(1,10) for x in range(-PREC//2, PREC//2)]
pprint.pprint(list(float(f) for f in fs))
for n in tqdm(range(1, N, N // 10)):
    pyplot.plot(fs, [expected_utility(f, utility_log_log, n) for f in fs], label=str(n))
pyplot.axvline(x=kelly_fraction)
pyplot.legend()
pyplot.show()