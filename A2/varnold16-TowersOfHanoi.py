#!/usr/bin/python3

# Exercise A2 Towers of Hanoi

"""
The task is to solve the n-disc Towers of Hanoi puzzle.

Implement a program that accepts an integer via command line option __-n__ and prints instructions to STDOUT as follows:

Move disk from X to Y

Likewise, the tool should print the total number of disc move operations
to STDERR upon finishing the computation. Allow the user to obtain some information on your tool via a __--help__
option. The program should be named as

*` $githubusername-TowersOfHanoi.$suffix -n [--help]`

Measure the runtime of your tool, ensuring that STDOUT is redirected to a file rather than displayed via the console
(which would unnecessarily blow up runtime). You might employ the concept of subshells to get this done.

Plot the runtime of your program (in seconds) vs size of the Hanoi puzzle and create a PDF graph. Your pull request
should include the following files:

* your program
* A file containing STDOUT of your program up to at least n=25. The name of this file should be
`$githubusername-TowersOfHanoi.out`
* a PDF plot of runtime vs n named `$githubusername-TowersOfHanoi_runtime.pdf`
"""


from argparse import ArgumentParser
import sys


# set True in production
DEBUG = False


# declare ArgumentParser
parser = ArgumentParser(prog='./varnold16-TowersOfHanoi.py',
                        description='Program for solution of the \"Towers of Hanoi Puzzle\" with n disks.\n'
                                    'Gives out needed steps (move disk from peg to peg) to STDOUT and writes total'
                                    ' number of disc move operations to STDERR.\n')

parser.add_argument('-n', dest='numberOfDisks', type=int, required=True,
                    help='number of how many disks should be moved from peg to peg')


# hand over arguments
if DEBUG:
    args = parser.parse_args(['-n', '3'])

else:
    args = parser.parse_args()

nDisks = args.numberOfDisks


# define function
def hanoiTowers(numberOfDisks, fromPeg, toPeg):
    global countSteps
    if numberOfDisks == 1:
        print("Move disk from", fromPeg, "to", toPeg)
        countSteps += 1
        return
    unusedPeg = 6 - fromPeg - toPeg
    hanoiTowers(numberOfDisks - 1, fromPeg, unusedPeg)
    print("Move disk from", fromPeg, "to", toPeg)
    hanoiTowers(numberOfDisks - 1, unusedPeg, toPeg)
    countSteps += 1
    return


# run program
countSteps = 0

hanoiTowers(nDisks, 1, 3)

sys.stderr.write(str(countSteps)+"\n")

