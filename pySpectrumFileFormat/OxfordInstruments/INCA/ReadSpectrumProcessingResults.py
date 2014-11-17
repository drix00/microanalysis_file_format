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
__svnId__ = "$Id: ReadSpectrumProcessingResults.py 2293 2011-03-21 18:39:25Z hdemers $"

# Standard library modules.

# Third party modules.

# Local modules.

# Globals and constants variables.

class ReadSpectrumProcessingResults(object):
    _HEADERSTRING = "Fit index"

    def __init__(self, filepath):
        self.data = {}

        self.read(filepath)

        if len(self.data) == 0:
            raise ValueError

    def read(self, filepath):
        lines = open(filepath, 'r').readlines()

        self._extractData(lines)

    def _extractData(self, lines):
        if self._HEADERSTRING not in lines[0]:
            raise ValueError

        data = {}

        line = lines[0].strip()
        headers = line.split("\t")

        for line in lines[1:]:
            line = line.strip()

            if len(line) == 0:
                continue

            items = line.split("\t")

            if len(items) == 6:
                for index,item in enumerate(items[:3]):
                    data.setdefault(headers[index], []).append(item)

                for index,item in enumerate(items[3:]):
                    try:
                        data.setdefault(headers[index+3], []).append(float(item))
                    except ValueError:
                        data.setdefault(headers[index+3], []).append(0.0)

            elif len(items) == 5:
                data.setdefault(headers[0], []).append("")

                for index,item in enumerate(items[:2]):
                    data.setdefault(headers[index+1], []).append(item)

                for index,item in enumerate(items[2:]):
                    try:
                        data.setdefault(headers[index+3], []).append(float(item))
                    except ValueError:
                        data.setdefault(headers[index+3], []).append(0.0)

        self.data = data
        self.headers = headers

def isValidFile(filepath):
    isValid = False

    try:
        ReadSpectrumProcessingResults(filepath)

        isValid = True
    except ValueError:
        isValid = False

    return isValid

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
