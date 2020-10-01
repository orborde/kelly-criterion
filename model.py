#! /usr/bin/env python3

import random

bankroll=100.
fraction=0.75
outcomes = [-1, 1.1]

ct = 0
while True:
    ct += 1
    bet = bankroll * fraction
    outcome = random.choice(outcomes)*bet
    bankroll += outcome

    if ct % 1 == 0:
        print(ct, bankroll)
