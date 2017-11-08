# This is like the other script, but explores how quickly bowls are filled with different spoon sizes

import matplotlib.pyplot as plt
import numpy as np

# Set our initial variables
BOWL_SIZE = 500 # maximum bowl size
INITIAL_SOUP_AMOUNT = [ 100, 200, 300, 400 ] # initial amount of each soup in each bowl

def is_soup_done(soup):
    ratio = float(soup[0]) / (soup[0] + soup[1])
    return (ratio >= .45 and ratio <= .55)

def can_fill_soup(soup, spoonsize):
    return (soup[0] + soup[1] + spoonsize) < BOWL_SIZE

def get_spoon(soup, spoonsize):
    ratio = float(soup[0]) / (soup[0] + soup[1])
    return [spoonsize * ratio, spoonsize * (1 - ratio)]

def swap_index(idx):
    return 0 if idx == 1 else 1

def solve_soup_backandforth(soups, spoonsize):
    spoonCount = 0
    soupIdx = 0
    while not (is_soup_done(soups[0]) or is_soup_done(soups[1])):
        spoon = get_spoon(soups[soupIdx], spoonsize)
        if can_fill_soup(soups[soupIdx], spoonsize):
            soups[soupIdx][0] -= spoon[0]
            soups[soupIdx][1] -= spoon[1]
            soups[swap_index(soupIdx)][0] += spoon[0]
            soups[swap_index(soupIdx)][1] += spoon[1]
            spoonCount += 1
        soupIdx = swap_index(soupIdx)
    return spoonCount

solve_speed = [[],[],[],[]]
