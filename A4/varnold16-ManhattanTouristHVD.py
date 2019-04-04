#!/usr/bin/python3

# Exercise A4 Manhattan Tourist Problem - Part 2

"""
# Aufgabe A4
## Manhattan Tourist Problem - Part 2

This assignment builds on the previous task to solve the Manhattan Tourist Problem for horizontal and vertical edges.
The new task is to extend your existing tool to also consider diagonal edge weights.

As you can expect, we need additional input for that. In particular, a (N-1)\*(N-1) matrix containing diagonal edge
weights. The input files for this assignment naturally extend the horizontal/vertical (HV) with a third matrix
(horizonal/vertical/diagonal HVD):

```
G_down: 4 5
  0.60   0.65   0.91   0.94   0.14
  0.85   0.27   0.70   0.31   0.63
  0.63   0.23   0.35   0.77   0.20
  0.37   0.76   0.41   0.30   0.67
---
G_right: 5 4
  0.76   0.41   0.72   0.13
  0.57   0.64   0.62   0.62
  0.37   0.98   0.36   0.24
  0.99   0.77   0.39   0.35
  0.37   0.34   0.62   0.82
---
G_diag: 4 4
  6.74   7.03   2.47   6.25
  4.48   3.75   2.98   3.62
  7.90   3.63   3.67   3.18
  9.30   8.40   9.02   2.58
---
```

In practice, this boils down to add another check in your dynamic programming algorithm and complements the forward
algorithm required to compute a global sequence alignment of two strings (which will be the next task A5).

You should select another pair of input matrices from the *rmHVD_10_X* and *rmHV_999_X* set and use it as input of your
extended Manhattan Tourist implementation. All specifications from A3 apply here, i.e. your tool should be named
*$githubusername-ManhattanTouristHVD.$suffix* and read from STDIN as follows:

*$githubusername-ManhattanTouristHVD.$suffix < rmHVD_10_5*

Again, your tool should parse the dimension of the input matrix from the first data line of the input file, without
explicit requirement to pass the dimension at runtime (see A3).

Your pull request should include the following:

* your program (source code) that can process HVD Manhattan grids
* weight of the longest path for your input files (one for dim 10, and one for dim 999, respectively)
* two input files you selected. Let me know which file you chose in your ping message, e.g.
  `@mtw please review rmHVD_10_5`

**Submission due date is 8 April 2019 10:00 CEST**
"""

import fileinput

catFile = fileinput.input()  # via command $ cat filename | probe.py

verbose = False  # set true for print-commands of dictionary


def getWeights(matrixFile):
    """
    Returns two dictionaries with lines as keys (starting at 0 for G_down/_right) and values in a list for the value.
    :param matrixFile: "string filename"
    :return: sideDict = {line : [values]} for vertical (downsideDict) /  horizontal (rightsideDict) edge weights.
    """

    downsideDict = {}
    rightsideDict = {}
    diagonalDict = {}
    downside = False             # vertical
    rightside = False            # horizontal
    diagonal = False            # horizontal


    for line in matrixFile:

        if line.startswith("-") or line == '\n':
            pass

        elif line.startswith("G_down"):
            lineNumber = 0
            downside = True

        elif line.startswith("G_right"):
            lineNumber = 0
            downside = False
            rightside = True

        elif line.startswith("G_diag"):
            lineNumber = 0
            rightside = False
            diagonal = True

        else:
            if downside:
                if line.startswith("G"):
                    pass
                elif line.startswith("-"):
                    pass
                else:
                    lineNumber += 1
                    downsideDict[lineNumber-1] = line.strip("  ").strip(" \n").split("   ")

            if rightside:
                if line.startswith("-"):
                    break
                else:
                    lineNumber += 1
                    rightsideDict[lineNumber-1] = line.strip("  ").strip(" \n").split("   ")

            if diagonal:
                if line.startswith("-"):
                    break
                else:
                    lineNumber += 1
                    diagonalDict[lineNumber-1] = line.strip("  ").strip(" \n").split("   ")

    return rightsideDict, downsideDict, diagonalDict



def manhattanTourist(down, right, diag):
    """
    Finds weight of longest path in a N\*N-grid with (N-1)\*N horizontal, N\*(N-1) vertical and (N-1)\*(N-1) edges.
    :param down: dictionary with N-1 keys, list per key of weights between one row and the another (N vertical edges).
    :param right: dictionary with N keys, list per key of weights between columns (N-1 horizontal edges).
    :return: wheight of the longest path
    """
    n = len(right)
    m = len(down[0])

    matrixDict = {}

    matrixDict[(0, 0)] = 0

    for i in range(0, m):
        for j in range(0, n):
            matrixDict[(m, n)] = 0

    for i in range(1, m):                                                  # down - first column
        matrixDict[(i, 0)] = matrixDict[(i-1, 0)] + float(down[i-1][0])

    for j in range(1, m):                                                  # right - first row
        matrixDict[(0, j)] = matrixDict[(0, j-1)] + float(right[0][j-1])

    for i in range(1, n):
        for j in range(1, m):
            matrixDict[(i, j)] = \
                max((matrixDict[i-1, j] + float(down[i-1][j])),\
                    (matrixDict[i, j-1] + float(right[i][j-1])),\
                    (matrixDict[i-1, j-1] + float(diag[i-1][j-1])))

    if verbose:  # prints matrix of manhattan
        for i in range(0, n):
            for j in range(0, m):
                print("("+str(i)+","+str(j)+") "+str(round(matrixDict[(i, j)],1)))

    return matrixDict[(n-1, m-1)]


(rightsideDict, downsideDict, diagonalDict) = getWeights(catFile)

maximum = manhattanTourist(downsideDict, rightsideDict, diagonalDict)

print(round(maximum, 2))


if verbose:  # prints dictionary of parsed file
    print("downside: ", len(downsideDict), len(downsideDict[0]))

    for key in downsideDict:
        print(key, downsideDict[key])

    print("rightside:", len(rightsideDict), len(rightsideDict[0]))

    for key in rightsideDict:
        print(key, rightsideDict[key])
