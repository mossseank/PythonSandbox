# Solves the problem as to if it is faster to mix two soups, using only a single spoon, by:
# 1. Alternatively spooning the soups back and forth, or...
# 2. Completely filling one bowl, then the other
# The metric for completion is acheiving a 55:45 ratio, where the originally dominant soup is the 55
# This problem was posed by my friend Ian, who got concerned about a football player who apparently did this on a date

import matplotlib.pyplot as plt
import numpy as np
import os

BOWL_SIZE = 100 # maximum bowl size
INITIAL_SOUP_AMOUNT = 60 # initial amount of each soup in each bowl
SPOON_SIZE = 4 # amount of soup a spoon can hold (try to keep this a factor of BOWL_SIZE)
SOUP_NAMES = ['broccoli', 'cheddar'] # very important for this problem

# bowls are a tuple of the amounts of each of the two soups
soups = [[INITIAL_SOUP_AMOUNT, 0], [0, INITIAL_SOUP_AMOUNT]]

def is_soup_done(soup):
    ratio = float(soup[0]) / (soup[0] + soup[1])
    return (ratio >= .45 and ratio <= .55)

def is_soup_full(soup):
    return (soup[0] + soup[1]) >= BOWL_SIZE

def can_fill_soup(soup):
    return (soup[0] + soup[1] + SPOON_SIZE) < BOWL_SIZE

def get_spoon(soup):
    ratio = float(soup[0]) / (soup[0] + soup[1])
    return [SPOON_SIZE * ratio, SPOON_SIZE * (1 - ratio)]

def swap_index(idx):
    return 0 if idx == 1 else 1

while True:
    rawin = input('Please enter the type of mixing (1/2):')
    try:
        mixtype = int(rawin)
    except:
        print('Please enter a number')
        continue
    if mixtype == 1 or mixtype == 2:
        break
    print('Please enter a valid number')

soup_history = [[],[],[],[]]
spoonCount = 0
if mixtype == 1:
    soupIdx = 0
    while not (is_soup_done(soups[0]) or is_soup_done(soups[1])):
        spoon = get_spoon(soups[soupIdx])
        if can_fill_soup(soups[soupIdx]):
            soups[soupIdx][0] -= spoon[0]
            soups[soupIdx][1] -= spoon[1]
            soups[swap_index(soupIdx)][0] += spoon[0]
            soups[swap_index(soupIdx)][1] += spoon[1]
            soup_history[0].append(soups[0][0])
            soup_history[1].append(soups[0][1])
            soup_history[2].append(soups[1][0])
            soup_history[3].append(soups[1][1])
            spoonCount += 1
        soupIdx = swap_index(soupIdx)
    print ('Soup was balanced after %d spoonfulls.' % (spoonCount))

else:
    soupIdx = 0
    while not is_soup_done(soups[soupIdx]):
        while can_fill_soup(soups[swap_index(soupIdx)]) and not is_soup_done(soups[swap_index(soupIdx)]):
            spoon = get_spoon(soups[soupIdx])
            soups[soupIdx][0] -= spoon[0]
            soups[soupIdx][1] -= spoon[1]
            soups[swap_index(soupIdx)][0] += spoon[0]
            soups[swap_index(soupIdx)][1] += spoon[1]
            soup_history[0].append(soups[0][0])
            soup_history[1].append(soups[0][1])
            soup_history[2].append(soups[1][0])
            soup_history[3].append(soups[1][1])
            spoonCount += 1
        soupIdx = swap_index(soupIdx)
    print ('Soup was balanced after %d spoonfulls.' % (spoonCount))

# Plot the results
fig1 = plt.figure(1, figsize=(11, 8.5))
plt.style.use('ggplot')
x = np.arange(0, spoonCount, 1)
plt.suptitle('Important Soup Questions', fontsize=16)
plt.title('Bowl Cap. = %.2f units, Initial Soup Cap. = %.2f units, Spoon Cap. = %.2f units' % 
    (BOWL_SIZE, INITIAL_SOUP_AMOUNT, SPOON_SIZE), fontsize=6)
plt.ylabel('Volume Units of Soup')
plt.xlabel('Spoonfulls')
plt.plot(x, soup_history[0], label='Amount of %s soup in Bowl 1' % (SOUP_NAMES[0]))
plt.plot(x, soup_history[1], label='Amount of %s soup in Bowl 1' % (SOUP_NAMES[1]))
plt.plot(x, soup_history[2], label='Amount of %s soup in Bowl 2' % (SOUP_NAMES[0]))
plt.plot(x, soup_history[3], label='Amount of %s soup in Bowl 2' % (SOUP_NAMES[1]))
plt.plot(x, [sum(x) for x in zip(soup_history[0], soup_history[1])], label='Total Soup in Bowl 1', linestyle='--',
    linewidth=1)
plt.plot(x, [sum(x) for x in zip(soup_history[2], soup_history[3])], label='Total Soup in Bowl 2', linestyle='--',
    linewidth=1)
plt.axvline(x=spoonCount-1, ymin=0.25, ymax=0.75, linestyle='--', c='k', linewidth=2)
ylim = plt.gca().get_ylim()
xlim = plt.gca().get_xlim()
plt.text(spoonCount-(0.075*(xlim[1]-xlim[0])), 0.225*(ylim[1]-ylim[0])+ylim[0], 'Final: %d spoonfulls' % (spoonCount),
    bbox=dict(facecolor='gray', alpha=0.5))
plt.legend()
if not os.path.isdir('./img'):
    os.mkdir('./img')
plt.savefig('./img/%d.%d.%d.%d.soup.png' % (BOWL_SIZE, INITIAL_SOUP_AMOUNT, SPOON_SIZE, mixtype), dpi=300)
# plt.show()