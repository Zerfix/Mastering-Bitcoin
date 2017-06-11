#!/bin/env python2.7

# max money

start_block_reward = 50

reward_interval = 210000

def max_money():
    current_reward = 50 * 10 ** 8
    total = 0
    while current_reward > 0:
        total += reward_interval * current_reward
        current_reward /= 2
    return total

print "Total BTC to ever be created:", max_money(), "Satoshis"