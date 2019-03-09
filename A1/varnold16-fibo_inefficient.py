#!/usr/bin/python3

# Exercise A1 Fibonacci numbers efficient

"""
The task is to compute the the first *n* Fibonacci numbers. Implement an ineffieient as well as an efficient version as
two standalone programs that should accept an integer via command line option __-n__ and print the nth Fibonaci number
to STDOUT. Implement an optional command line switch __--all__ that prints all Fibonacci numbers up to n as a
comma-separated list to STDOUT. Document your tools accordingly, i.e. provide at least a __--help__ switch that prints
simple usage instructions to STDOUT. The file must be named according
to the following schema:

* $githubusername-fibo_inefficient.$suffix -n <int> [--all] [--help]
* $githubusername-fibo_efficient.$suffix -n <int> [--all] [--help]

Measure the runtime of both tools for different parameters of n, e.g. via the `time` command. Plot the runtime of both
approaches as a function of n in a single PDF graph. The filename should be `$githubusername-fibo_runtime.pdf`.
"""


from argparse import ArgumentParser


# Set True in production
DEBUG = False


# declare ArgumentParser
parser = ArgumentParser(prog='./varnold16-fibo_efficient.py',
                        description='Gives the last/all number/s of the Fibonacci sequence with n steps.\n'
                                    'Beginning with 0 (no step made), doing n steps and gaining n+1 numbers.')

parser.add_argument('-n', dest='steps', type=int, required=True,
                    help='number of how many steps shall be made')

parser.add_argument('--all', action='store_true',
                    help='show all numbers of the Fibonacci sequence with n-steps as array')


# hand over arguments
if DEBUG:
    args = parser.parse_args(['-n', '10'])
    #args = parser.parse_args(['-n', '10', '--all'])

else:
    args = parser.parse_args()

steps = args.steps


# gaining n+1 numbers of Fibonacci sequence with n steps
fibonacci_numbers = list()                                                          # will contain all gained numbers

for i in range(0, steps + 1):
    fibonacci_numbers.append(i)


def get_fibonacci_number(number_of_steps, number_list=list()):

    if number_of_steps == 0:                                                        # no step / beginning
        return 0

    elif number_of_steps == 1:                                                      # first step / at least 1 step
        return 1

    else:                                                                           # > 1 step
        number_a = get_fibonacci_number(number_of_steps - 1, number_list)
        number_b = get_fibonacci_number(number_of_steps - 2, number_list)
        result = number_a + number_b
        number_list[number_of_steps] = result
        return result


get_fibonacci_number(steps, fibonacci_numbers)


# output
if args.all:
    print(*fibonacci_numbers, sep=", ")

else:
    print(fibonacci_numbers[steps])
