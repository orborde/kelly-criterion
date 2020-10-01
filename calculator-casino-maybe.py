import random

bankroll = 100
fraction = .75

def game(bankroll, bet):
    bankroll -= bet
    mul = sum(random.random() for _ in range(4)) / 3
    bet *= mul
    bankroll += bet
    return bankroll, mul, bet

ct=0
while True:
    bet = fraction * bankroll
    print ct, bankroll, bet,
    bankroll, mul, returned = game(bankroll, bet)
    print '->', mul, returned, '=', bankroll
    ct += 1
