# This script produces a plot of the stopping length of the collatz sequence for a range of inputs
# No arguments defaults to (1, 100,000) as the range
#   - 1 arg range (1, arg)
#   - 2 arg range (arg1, arg2)
#   - 3 arg range (arg1, arg2), with arg3 being the step

from collatz import collatz
import sys
import numpy as np
import multiprocessing as mproc
from time import perf_counter as timer_f
import matplotlib.pyplot as plt
import os

def _parse_positive_int(arg, argnum):
    try:
        val = int(arg)
        if val >= 1:
            return val
        print('Could not parse argument {}: not a non-zero, positive integer'.format(argnum))
    except:
        print('Could not parse argument {}: not a valid integer'.format(argnum))
    sys.exit(-argnum)


# Multiprocessing function
def _collatz_finder(value):
    res = collatz(value)
    return (value, res[0])


def _main():
    # Parse the arguments
    arg_len = len(sys.argv)
    _START = 1
    _END = 100000
    _STEP = 1
    if arg_len == 2:
        _END = _parse_positive_int(sys.argv[1], 1)
    elif arg_len == 3:
        _START = _parse_positive_int(sys.argv[1], 1)
        _END = _parse_positive_int(sys.argv[2], 2)
    elif arg_len >= 4:
        _START = _parse_positive_int(sys.argv[1], 1)
        _END = _parse_positive_int(sys.argv[2], 2)
        _STEP = _parse_positive_int(sys.argv[3], 3)
    if _END < _START:
        print('Cannot have the end of the range before the start of the range')
        sys.exit(-1)
    _COUNT = int((_END - _START) // _STEP + 1)
    print('Using range ({}, {}), step {}, total {}'.format(_START, _END, _STEP, _COUNT))

    # Figure out multiprocessing
    _MULTIPROC = _COUNT >= 50_000 and mproc.cpu_count() > 1
    if _MULTIPROC:
        print('Using multiprocessing on {} cores'.format(mproc.cpu_count()))

    # Calculate the sequences
    inputs = range(_START, _END + 1, _STEP)
    outputs = np.zeros((_COUNT, 2), dtype=int)
    start_time = 0.
    end_time = 0.
    if _MULTIPROC:
        calc_pool = mproc.Pool(mproc.cpu_count())
        start_time = timer_f()
        res = calc_pool.map(_collatz_finder, inputs)
        end_time = timer_f()
        calc_pool.close()
        for ii, val in enumerate(res):
            outputs[ii] = val
    else:
        start_time = timer_f()
        for i, coll_in in enumerate(inputs):
            outputs[i][0] = coll_in
            outputs[i][1] = collatz(coll_in)[0]
        end_time = timer_f()
    print('Finished calculating in {:.3f} seconds'.format(end_time - start_time))

    # Generate info about the numbers
    min_coll = outputs[np.argmin(outputs[:,1])]
    max_coll = outputs[np.argmax(outputs[:,1])]
    x_range = _END - _START
    y_range = max_coll[1] - min_coll[1]
    y_min = min_coll[1]
    shift_size = (0.004 * x_range, 0.004 * y_range)

    # Get the graph type
    gtype = 0
    while True:
        gtype = input('Enter the plot type to use (0=linear [default], 1=log) > ').strip()
        if len(gtype) == 0:
            break
        try:
            gtype = int(gtype)
            if gtype == 0 or gtype == 1:
                break
            print('Please enter a valid number')
        except:
            print('Please enter a valid number')
            continue

    # Generate the graph
    print('Generating and saving graph...')
    start_time = timer_f()
    plt.style.use('ggplot')
    fig, axs = plt.subplots(1, 1, figsize=(11, 8.5))
    fig.suptitle('Collatz Stopping Numbers', fontsize=18)
    axs.set_title('Start: {}  End: {}  Step: {}'.format(_START, _END, _STEP), fontsize=10)
    axs.set_xlabel('Input [n]')
    axs.set_ylabel('Collatz(n)')
    axs.scatter(outputs[:,0], outputs[:,1], s=6)
    if gtype == 1:
        axs.set_xscale('log')
    axs.text(max_coll[0] + shift_size[0], max_coll[1] + shift_size[1], 'Max: ({}, {})'.format(*max_coll))
    axs.text(min_coll[0] + shift_size[0], min_coll[1] - shift_size[1], 'Min: ({}, {})'.format(*min_coll), verticalalignment='top')
    if not os.path.isdir('./img/stop'):
        os.makedirs('./img/stop')
    fig.savefig('./img/stop/{}.{}.{}.png'.format(_START, _END, _STEP))
    end_time = timer_f()
    print('Complete ({:.1f} ms)'.format((end_time - start_time) * 1000))

if __name__ == '__main__':
    _main()
