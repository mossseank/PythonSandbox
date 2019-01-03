This project looks at the collatz conjecture (https://en.wikipedia.org/wiki/Collatz_conjecture).

The collatz sequence, starting from a number, iterates based off of the simple rule: if the number is even, divide by two, if its odd, multiply by three and add one. The collatz conjecture says that this sequence will always end at one for all inputs. It is an unproven conjecture (although most everyone expects it to be true), and despite how simple it is, many mathmeticians believe that it cannot be proven using any of our current mathematical structures or concepts.

* `collatz.py` - Contains functions for calculating collatz sequences and information about them
* `stopping_number.py` - Calculates the stopping number (collatz sequence length) for ranges of inputs, and plots them
  * Valid arguments: `stopping_number.py <end>`, `stopping_number.py <start> <end>`, `stopping_number.py <start> <end> <step>`
  * No arguments defaults to 1 to 100,000 as the range, with a step size of 1