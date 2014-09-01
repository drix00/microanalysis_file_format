#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2293 $"
__svnDate__ = "$Date: 2011-03-21 14:39:25 -0400 (Mon, 21 Mar 2011) $"
__svnId__ = "$Id: ReadSpectrumFullResults.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class ReadSpectrumFullResults(object):
    _KEYWORD_SEPERATOR = ":"

    _SAMPLE_POLISHED_COMMENT = "Sample is polished"

    _SAMPLE_UNCOATED_COMMENT = "Sample is uncoated"

    _ELEMENT_OPTIMIZATION_COMMENT = "The element used for optimization"

    _ELEMENT = "k ratio"

    _TOTALS = "Totals"

    def __init__(self, filepath):
        self.comments = []
        self.data = {}

        self.read(filepath)

        if len(self.data) == 0:
            raise ValueError

    def read(self, filepath):
        lines = open(filepath, 'r').readlines()

        self._extractData(lines)

    def _extractData(self, lines):
        readElementsState = False

        data = {}
        for line in lines:
            line = line.strip()

            if len(line) == 0:
                continue

            if self._KEYWORD_SEPERATOR in line and not readElementsState:
                self._extractKeywordValue(line)
                readElementsState = False
            elif self._SAMPLE_POLISHED_COMMENT in line:
                self._addComment(line)
                readElementsState = False
            elif self._SAMPLE_UNCOATED_COMMENT in line:
                self._addComment(line)
                readElementsState = False
            elif self._ELEMENT_OPTIMIZATION_COMMENT in line:
                self._addComment(line)
                readElementsState = False
            elif self._ELEMENT in line:
                headers = self._extractHeader(line)
                self.headers = headers
                readElementsState = True
            elif self._TOTALS in line:
                data["Totals"] = self._extractTotalsData(line)
                readElementsState = False
            elif readElementsState:
                label, newData = self._extractSpectrumData(line)
                data[label] = newData
            else:
                #print line
                pass

        self.data = data

    def _extractSpectrumData(self, line):
        items = line.split("\t")

        label = items[0]

        values = []

        # Line.
        values.append(items[1])

        # Skip label.
        for item in items[2:8]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        for item in items[8:]:
            values.append(item)

        return label, values

    def _extractHeader(self, line):
        items = line.split("\t")

        values = []

        for item in items:
            try:
                value = str(item)

                values.append(value)
            except ValueError:
                pass

        return values

    def _extractTotalsData(self, line):
        items = line.split("\t")

        totals = float(items[-1])

        return totals

    def _extractLineData(self, line):
        items = line.split("\t")

        values = []

        # Skip label.
        for item in items[1:]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        return values

    def _extractKeywordValue(self, line):
        # TODO: Implement
        pass

    def _addComment(self, line):
        self.comments.append(line)

def isValidFile(filepath):
    isValid = False

    try:
        ReadSpectrumFullResults(filepath)

        isValid = True
    except ValueError:
        isValid = False

    return isValid

if __name__ == '__main__': #pragma: no cover
    import DrixUtilities.Runner as Runner
    Runner.Runner().run(runFunction=None)
