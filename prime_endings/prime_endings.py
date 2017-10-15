# A small script used to calculate the relations between the ending digit(s) of the prime numbers
# This topic is explored in the Numberphile video: https://www.youtube.com/watch?v=YVvfY_lFUZ8

import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from prettytable import PrettyTable

PRIME_FILE = '../_data/primes/first1e6.dat'


# Load in the first 1 million primes (from generated file)
if not os.path.isfile(PRIME_FILE):
    print('Please make sure to generate the data file for the first 1e6 primes.')
    sys.exit(1)
primes = np.zeros(1000000, dtype=int)
with open(PRIME_FILE, 'r') as primefile:
    primefile.readline() # Read past comment line
    index = 0
    for line in primefile:
        primes[index] = int(line)
        index += 1
    if index != 1000000:
        print('The data file did not contain 1 million primes')
        sys.exit(1)

# Get the last digit for all of the primes
ALLOWED_DIGITS = [2, 5, 1, 3, 7, 9]
pdigits = np.zeros(1000000, dtype=int)
for i, prime in enumerate(primes):
    pdigits[i] = (prime % 10)

# Report the percentages of digits as they appear
digit_perc = np.zeros(6)
dperc_table = PrettyTable(['Digit', 'Percentage'])
for i, adigit in enumerate(ALLOWED_DIGITS):
    digit_perc[i] = (pdigits == adigit).sum() / 1e6
    dperc_table.add_row([adigit, '%.3f%%' % (digit_perc[i] * 100.0)])
print('\n  Digit Distribution')
print(dperc_table)

# Remove the 2 and 5
primes = np.concatenate(([3], primes[3:]))
pdigits = np.concatenate(([3], pdigits[3:]))

# Calculate and report the percentages of digit pairs
dpairs_perc = np.zeros((4, 4))
dpairs_values = [1, 3, 7, 9]
mapindex = [0, 0, 0, 1, 0, 0, 0, 2, 0, 3]
def _pairmap(d1, d2):
    return (mapindex[d1], mapindex[d2])
for i in range(len(primes) - 1):
    (d1, d2) = pdigits[i:i+2]
    dpairs_perc[_pairmap(d1, d2)] += (1 / 1e6)
dpairs_table = PrettyTable(['', 1, 3, 7, 9])
for i in range(4):
    dpair_fmt = ['%.3f%%' % (perc * 100) for perc in dpairs_perc[i]]
    dpairs_table.add_row(np.concatenate(([dpairs_values[i]], dpair_fmt)))
print('\n            Pair Distribution')
print(dpairs_table)
