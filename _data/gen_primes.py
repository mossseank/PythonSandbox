# This is a script that will find prime numbers, either as a first-N primes functionality, or an
#   all-less-than-N primes functionality. In both instances, it uses the Seive of Erathosthenes,
#   using a bitset as the primeset to check against, making it efficient in both performance and
#   memory. However, since the SoE requires an upper limit known at start time, we use Rosser's
#   Theorem to calculate an upper bound on the value of the nth prime number. This provides an
#   always valid, but potentially less memory efficient method of calculating the first N primes.

from bitarray import bitarray as bitarr
import sys
import os
import math
import time


__lasttime = 0
def get_last_gen_time():
    global __lasttime
    return __lasttime


# https://en.wikipedia.org/wiki/Rosser%27s_theorem
def __rosser(n):
    logn = math.log(n)
    return int(n * logn * math.log(logn))


def gen_primes(count, method='lt'):
    global __lasttime
    if not isinstance(count, int):
        raise RuntimeError('The value passed to gen_primes must be an int')

    plimit = count
    if method == 'first':
        count = __rosser(count)
    elif method != 'lt':
        raise RuntimeError('Only the methods "lt" and "first" are valid for gen_primes')

    starttime = time.perf_counter()
    limit = count + 1
    checkarr = bitarr(limit)
    checkarr.setall(True)
    checkarr[0:2] = False # 0 and 1 don't count

    passlimit = int(math.sqrt(limit)) + 1
    for i in range(2, passlimit + 1):
        if checkarr[i]:
            for j in range(i * i, limit, i): # Include prime's square optimization
                checkarr[j] = False

    pcnt = 0
    for value in range(limit):
        if pcnt == plimit:
            break
        if checkarr[value]:
            yield value
            pcnt += 1

    __lasttime = (time.perf_counter() - starttime)


def __main(argv):
    N = 0
    if len(argv) < 2:
        N = input('Number of primes, or limit: ')
    else:
        N = argv[1]

    try:
        N = int(N)
    except ValueError:
        print('Please enter a valid integer number for the number of primes to generate')
        return

    filename = 'primes.txt'
    if len(argv) < 3:
        filename = input('Output file name: ')
    else:
        filename = argv[2]

    filename = filename.strip()
    if len(filename.strip()) == 0:
        print('Cannot use an empty file name')
        return

    if os.path.isfile(filename):
        print('The file %s already exists, cannot overwrite it' % (filename))
        return

    method = 'lt'
    if len(argv) < 4:
        method = input('Method for gen_primes: ')
    else:
        method = argv[3]

    with open(filename, 'w') as outFile:
        outFile.write('# First %d primes\n' % (N))
        for prime in gen_primes(N, method):
            outFile.write('%d\n' % (prime))

    print('Complete! Generation took %.5f seconds.' % (__lasttime))


if __name__ == '__main__':
    __main(sys.argv)
