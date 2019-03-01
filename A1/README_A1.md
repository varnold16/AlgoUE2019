# Aufgabe A1
# Fibonacci numbers

The task is to compute the the first *n* Fibonacci numbers. Implement an ineffieient as well as an efficient version as two standalone programs that should accept an integer via command line option __-n__ and print the nth Fibonaci number to STDOUT. Implement an optional command line switch __--all__ that prints all Fibonacci numbers up to n as a comma-separated list to STDOUT.

* fibo_inefficient -n <int> [--all]
* fibo_efficient -n <int> [--all]

Measure the runtime of both tools for different parameters of n, e.g. via the `time` command. Plot the runtime of both approaches as a function of n in a single PDF graph. The filename should be `fibo_runtime.pdf`.
