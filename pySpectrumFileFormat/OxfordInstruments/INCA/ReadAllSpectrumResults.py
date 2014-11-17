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
__svnId__ = "$Id: ReadAllSpectrumResults.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class ReadAllSpectrumResults(object):
    _KEYWORD_SEPERATOR = ":"

    _NORMALISED_COMMENT = "All elements analyzed (Normalised)"

    _RESULTS_WEIGHT_PERCENT = "All results in Weight Percent"

    _MEAN = "Mean"
    _STD_DEV = "Std. dev."
    _MAX = "Max."
    _MIN = "Min."

    _SPECTRUM = "Spectrum Label"

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
        readSpectraState = False

        data = {}
        for line in lines:
            line = line.strip()

            if len(line) == 0:
                continue

            if self._KEYWORD_SEPERATOR in line:
                self._extractKeywordValue(line)
                readSpectraState = False
            elif self._NORMALISED_COMMENT in line:
                self._addComment(line)
                readSpectraState = False
            elif self._RESULTS_WEIGHT_PERCENT in line:
                self._addComment(line)
                readSpectraState = False
            elif self._MEAN in line:
                data["Mean"] = self._extractLineData(line)
                readSpectraState = False
            elif self._STD_DEV in line:
                data["StdDev"] = self._extractLineData(line)
                readSpectraState = False
            elif self._MAX in line:
                data["Maximum"] = self._extractLineData(line)
                readSpectraState = False
            elif self._MIN in line:
                data["Minimum"] = self._extractLineData(line)
                readSpectraState = False
            elif self._SPECTRUM in line:
                headers = self._extractSpectrumHeader(line)
                self.headers = headers
                readSpectraState = True
            elif readSpectraState:
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

        # Skip label.
        for item in items[1:]:
            try:
                value = float(item)

                values.append(value)
            except ValueError:
                pass

        return label, values

    def _extractSpectrumHeader(self, line):
        items = line.split("\t")

        values = []

        # Skip label.
        for item in items[1:]:
            try:
                value = str(item)

                values.append(value)
            except ValueError:
                pass

        return values

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
        ReadAllSpectrumResults(filepath)

        isValid = True
    except ValueError:
        isValid = False

    return isValid

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
