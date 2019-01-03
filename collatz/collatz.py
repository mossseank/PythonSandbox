# Functions for calculating the stopping value for the collatz conjecture
# More information on the collatz conjecture can be found at: https://en.wikipedia.org/wiki/Collatz_conjecture

from time import perf_counter

def collatz(start, limit=None):
    '''
    Runs through the collatz sequence for the input value.

    :param start int: The non-negative input integer to calculate the collatz sequence for.
    :param limit int: The number of iterations to calculate before giving up, or `None` for no limit.
    :returns tuple: (stop, limit_reached, evens, odds, time)
        - stop (int): the number of iterations before reaching 1 or the limit
        - limit_reached (bool): `True` if there was a limit and it was reached, `False` otherwise
        - evens (int): the number of even iterations in the sequence
        - odds (int): the number of odd iterations in the sequence
        - time (float): the time it took to calculate the collatz sequence, in milliseconds
    '''
    start = int(start)
    if start < 1:
        return (-1, False, -1, -1, -1)
    if limit is not None:
        limit = int(limit)

    iter = 0
    evens = 0
    odds = 0
    start_time = perf_counter()
    while start > 1 and (limit is None or iter >= limit):
        if start % 2 == 0: # even
            start = int(start // 2)
            iter += 1
            evens += 1
        else: # odd
            start = int(((3 * start) + 1) // 2) # Take a shortcut, make two steps at once because we can
            iter += 2
            evens += 1
            odds += 1
    
    end_time = perf_counter()
    return (iter, limit is not None and start != 1 and iter == limit, evens, odds, (end_time - start_time) * 1000)

if __name__ == '__main__':
    for i in range(1, 1001):
        coll = collatz(i)
        print ('collatz({}) = {}\t\t({}, {}, {})'.format(i, coll[0], coll[2], coll[3], coll[4]))
