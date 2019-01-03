# This script generates collatz sequences and plots them vs. iteration number
# It requires at least one argument, and can take up to 10

from collatz import collatz_gen
import sys
from time import perf_counter as timer_f
import matplotlib.pyplot as plt
import numpy as np
import os


def _parse_positive_int(arg, argnum):
    try:
        val = int(arg)
        if val >= 1:
            return val
        print('ERROR: Could not parse argument {}: not a non-zero, positive integer'.format(argnum))
    except:
        print('ERROR: Could not parse argument {}: not a valid integer'.format(argnum))
    sys.exit(-argnum)


def _main():
    # Parse in arguments
    in_len = len(sys.argv) - 1
    if in_len < 1:
        print('ERROR: At least one argument is required')
        sys.exit(1)
    elif in_len > 10:
        print('WARNING: More than 10 arguments provided, only using the first 10')
        in_len = 10
    inputs = [0] * in_len
    for i in range(in_len):
        inputs[i] = _parse_positive_int(sys.argv[i + 1], i)
    print('Generating {} sequences'.format(in_len))

    # Generate the sequences 
    start_time = timer_f()
    outputs = [collatz_gen(start) for start in inputs]
    end_time = timer_f()
    print('Generated in {:.3f} ms'.format((end_time - start_time) * 1000))

    # Create the plot
    print('Generating and saving plot...')
    start_time = timer_f()
    plt.style.use('ggplot')
    fig, axs = plt.subplots(1, 1, figsize=(11, 8.5))
    fig.suptitle('Collatz Sequences', fontsize=18)
    axs.set_title(('{}, ' * in_len).format(*inputs)[:-2], fontsize=10)
    axs.set_xlabel('Iteration Number [n]')
    axs.set_ylabel('Sequence at n')

    # Plot the values
    for (cin, cout) in zip(inputs, outputs):
        axs.plot(cout, label='{}'.format(cin))
    axs.set_yscale('log')
    fig.legend()
    xlim = axs.get_xlim()
    axs.axhline(1, xlim[0], xlim[1], color='black', linestyle='--')

    # Save
    if not os.path.isdir('./img/seq'):
        os.makedirs('./img/seq')
    plt.savefig('./img/seq/' + ('{}.' * in_len).format(*inputs) + 'png')
    end_time = timer_f()
    print('Completed in {:.1f} ms'.format((end_time - start_time) * 1000))


if __name__ == '__main__':
    _main()
