#!/usr/bin/env python3

"""
# Aufgabe A5
## Needleman-Wunsch pairwise global sequence alignment

The task in this assignment is to implement the Needleman-Wunsch (NW) algorithm for global alignment of two sequences.
This naturally extends the previous assignments (Manhattan Tourist Problem), i.e. you will need

* a scoring function for computing the similarity of two strings
* a backtracking method to compute the alignment

A simple default scoring function could be

* match: +1
* mismatch : -1
* gap: -2

and you are supposed to give the user the chance to change these numbers via command-line options **--match**,
**--mismatch** and **--gap**.

Your tool should read input sequences from a __multi-fasta__ file via STDIN. Such an input file could look like this:

```
>NC_006551.1 |DB.1|386-457|
CCACGGCCCAAGCGAACAGACGGTGATGCGAACTGTTCGTGGAAGGACTAGAGGTTAGAGGAG
ACCCCGTGG
>NC_035889.1 |DB.1|238-307|
CTGGGGCCTGAACTGGAGATCAGCTGTGGATCTCCAGAAGAGGGACTAGTGGTTAGAGGAGAC
CCCCCGG

```

Your tool should write the alignment to STDOUT in __Clustal__ format:

```
CLUSTAL


NC_006551.1            ccacggcccaagcgaacagacggtgatgcgaactgttcgtggaaggactagaggttagag
NC_035889.1            ctggggcctgaactggagatca--gctgtggatctccagaagagggactagtggttagag
                       *   ****  * *       *   * ** * *      *  ** ******* ********


NC_006551.1            gagaccccgtgg
NC_035889.1            gagaccccccgg
                       ********  **
```

Importantly, you are supposed to produce a decoration line for your alignment as shown above, i.e. print (below your
alignment) a __*__ for matching positions or a gap character for mismatches or indels. Each block in your alignment
should not contain more than 60 aligned positions. If your alignment is longer that 60 positions, introduce line wraps
as shown above. In addition, print the computed similarity value (result of the forward algorithm) to STDERR as a single
integer number.

Your tool should be named $githubusername-NW.$suffix and an example call should look like this:

* $githubusername-NW.$suffix --match __int__ --mismatch __int__ --gap __int__ [--help] < input.fa

Do not forget to provide a reasonable help message to you users, by adding a **--help** command line option.

Your pull request should include the following:

* your program (source code)

*Submission due date is 28 April 2019, 11:59PM*
"""

from argparse import ArgumentParser, FileType
import sys

# set True in production (a testsequence.fasta has to be in working directory), else False
DEBUG = False

# define ArgumentParser
parser = ArgumentParser(prog='varnold16-NW.py',
                        description="This program creates a pairwise global sequence alignment of sequences in fasta-"
                                    "format based on Needleman-Wunsch-Algorithm.")

parser.add_argument('stdin', nargs='?', type=FileType('r'), default=sys.stdin,
                    help='path to file as STDIN (via < filename or cat filename)')

parser.add_argument('--match', dest="match",
                    help='Score for matching of two single strings (+1 as default)', type=float, default="1")

parser.add_argument('--mismatch', dest="mismatch",
                    help='Score for mismatch of two single strings (-1 as default)', type=float, default="-1")

parser.add_argument('--gap', dest="gap",
                    help='Score for creating a gap (-2 as default)', type=float, default="-2")

if DEBUG:
    parser.add_argument('input', nargs='?',
                        help="name of fasta-file containing two sequences", type=str)

    args = parser.parse_args(['fasta.fasta', '--match', '10', '--mismatch', '-10', '--gap', '-20'])

    catFile = open(args.input, "r")

else:
    args = parser.parse_args()


inputFile = args.stdin
match = args.match
mismatch = args.mismatch
gap = args.gap


# converting fasta-file into dictionary
def getSequence(fastafile):
    """
    Creates a dictionary with header and sequence in a list of two elements of a fasta-file.
    :param fastafile: str - Name des fasta-Files
    :return: dict = {1 : [header, sequence], 2 : [header, sequence]}
    """

    sequences = {}
    sequence = []
    sequenceNumber = 0

    for line in fastafile:

        if line == '\n':
            pass

        else:
            if line.startswith(">"):
                if sequence == []:                             # header initialized, if no sequence
                    sequenceNumber += 1
                    header = line.strip("\n").split(" ")[0]
                    sequences[sequenceNumber] = [header]

                else:
                    sequences[sequenceNumber].append("".join(sequence))  # header, sequence-container are assigned
                    sequenceNumber += 1
                    header = line.strip("\n").split(" ")[0]
                    sequences[sequenceNumber] = [header]
                    sequence = []                              # sequence-container is emptied

            else:
                sequence.append(line.strip("\n"))              # line added to sequence-container

    sequences[sequenceNumber].append("".join(sequence))        # last entry (no following header)

    return sequences


def traceback(value1, value2, value3):
    """
    Returns single letter (D, H, V, U) to take note of direction to gain highest score.
    :param value1: value coming from diagonal
    :param value2: value coming from horizontal
    :param value3: value coming from vertical
    :return: "singleLetter" for indicating direction (to retrace path)
    """
    maximum = max(value1, value2, value3)

    if value1 == maximum:
        return "D"  # diagonal
    elif value2 == maximum:
        return "H"  # horizontal
    elif value3 == maximum:
        return "V"  # vertical
    else:
        return "U"  # unknown


def aligned(dictionaryWithSequences, scoreMatch=1, scoreMismatch=-1, scoreGap=2):
    """
    Searches best path to align to sequences (Needleman-Wunsch). Returns a list with score, aligned sequences including
    the header, and a decoration line marking matiching bases with a "*".
    :param dictionaryWithSequences: dictionary with 2 sequences {1 : [header, sequence], 2 : [header, sequence]}
    :param scoreMatch: score for a match (default = 1)
    :param scoreMismatch:  score for a mismatch (default = -1)
    :param scoreGap:  score for a gap(default = -2)
    :return: list = [[score, clustalSequence], [header1, alignedSequence1], [header2, alignedSequence2]]
    """
    sequence1 = dictionaryWithSequences[1][1]
    sequence2 = dictionaryWithSequences[2][1]

    n = len(sequence1) + 1                                     # dimension of the matrix columns.
    m = len(sequence2) + 1                                     # dimension of the matrix rows.

    scoringMatrix = {}

    traceMatrix = {}

    scoringMatrix[(0, 0)] = 0

    traceMatrix[(0, 0)] = "D"

    for i in range(0, m):
        for j in range(0, n):
            scoringMatrix[(m, n)] = 0
            traceMatrix[(m, n)] = 0

    # fill first row elements with "gap penalty"
    for i in range(m):
        scoringMatrix[(i, 0)] = scoreGap * i
        traceMatrix[(i, 0)] = "V"

    # fill first column elements with "gap penalty"
    for j in range(n):
        scoringMatrix[(0, j)] = scoreGap * j
        traceMatrix[(0, j)] = "H"

    # fill the matrix with the correct values.
    for i in range(1, m):
        for j in range(1, n):
            if sequence1[j-1] == sequence2[i-1]:               # diagonal -> mis-/match
                d = scoringMatrix[(i - 1, j - 1)] + scoreMatch
            else:
                d = scoringMatrix[(i - 1, j - 1)] + scoreMismatch

            h = scoringMatrix[(i, j-1)] + scoreGap             # horizontal -> gap in sequence1

            v = scoringMatrix[(i-1, j)] + scoreGap             # vertical -> gap in sequence2

            scoringMatrix[(i, j)] = max(d, h, v)               # fill matrix with the maximal value

            traceMatrix[(i, j)] = traceback(d, h, v)

    score = int(scoringMatrix[(i, j)])

    alignedSequence1 = ""
    alignedSequence2 = ""
    clustalSequence = ""

    # read path backwards from tracing matrix
    while(i > 0 or j >0):
        if traceMatrix[(i, j)] == "D":
            alignedSequence1 = sequence1[j-1] + alignedSequence1
            alignedSequence2 = sequence2[i-1] + alignedSequence2
            if sequence1[j-1] == sequence2[i-1]:
                clustalSequence = "*" + clustalSequence
            else:
                clustalSequence = " " + clustalSequence
            i -= 1
            j -= 1
        elif traceMatrix[(i, j)] == "H":
            alignedSequence1 = sequence1[j-1] + alignedSequence1
            alignedSequence2 = "-" + alignedSequence2
            clustalSequence = " " + clustalSequence
            j -= 1
        elif traceMatrix[(i, j)] == "V":
            alignedSequence1 = "-" + alignedSequence1
            alignedSequence2 = sequence2[i-1] + alignedSequence2
            clustalSequence = " " + clustalSequence
            i -= 1

    # create list to store output
    outputList = []
    outputList.append([score, clustalSequence])
    outputList.append([dictionaryWithSequences[1][0], alignedSequence1])
    outputList.append([dictionaryWithSequences[2][0], alignedSequence2])

    return outputList


def printSequences(outputList):
    """
    Reads out list of results gained from sequence alignment and prints it in clustal format
    :param outputList: list = [[score, clustalSequence], [header1, alignedSequence1], [header2, alignedSequence2]]
    :return: NO RETURN VALUE
    """
    sequence1 = outputList[1][1]
    sequence2 = outputList[2][1]
    clustalSequence = outputList[0][1]

    header1 = outputList[1][0]
    header2 = outputList[2][0]
    header1String = header1+" "*(20-len(header1))
    header2String = header2+" "*(20-len(header2))

    sequenceLength = len(clustalSequence)

    print("CLUSTAL"+"\n"+"\n")

    for i in range(sequenceLength // 60 + 1):
        print(header1String+sequence1[i * 60:i * 60 + 60])
        print(header2String+sequence2[i * 60:i * 60 + 60])
        print(" "*20+clustalSequence[i * 60:i * 60 + 60])


if __name__ == '__main__':

    if sys.stdin.isatty():
        parser.print_help()
    else:
        sequenceDictionary = getSequence(inputFile)

        resultList = aligned(sequenceDictionary, match, mismatch, gap)

        printSequences(resultList)

        sys.stderr.write(str(resultList[0][0])+"\n")  # write score to stderr
