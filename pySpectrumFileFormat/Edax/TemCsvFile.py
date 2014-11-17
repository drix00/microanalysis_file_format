#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2282 $"
__svnDate__ = "$Date: 2011-03-15 17:46:04 -0400 (Tue, 15 Mar 2011) $"
__svnId__ = "$Id: TemCsvFile.py 2282 2011-03-15 21:46:04Z hdemers $"

# Standard library modules.
import csv

# Third party modules.

# Local modules.

# Globals and constants variables.
CHANNEL = "Channel"
COUNTS = "Counts"

class TemCsvFile(object):
    def __init__(self, filepath):
        self._filepath = filepath

        self._data = self._readData(self._filepath)

    def _readData(self, filepath):
        reader = csv.reader(open(filepath, 'rU'))

        data = {}
        data.setdefault(CHANNEL, [])
        data.setdefault(COUNTS, [])

        for row in reader:
            channel = int(row[0])
            counts = int(row[1])

            data[CHANNEL].append(channel)
            data[COUNTS].append(counts)

        return data

    def getChannels(self):
        return self._data[CHANNEL]

    def getEnergies_eV(self, eVChannel_eV=10.0):
        return [xx*eVChannel_eV for xx in self._data[CHANNEL]]

    def getCounts(self):
        return self._data[COUNTS]

    def getData(self, eVChannel_eV=10.0):
        return self.getEnergies_eV(eVChannel_eV), self.getCounts()

if __name__ == '__main__':    #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=None)
