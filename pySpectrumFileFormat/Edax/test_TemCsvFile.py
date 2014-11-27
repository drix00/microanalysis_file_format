#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2009 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2280 $"
__svnDate__ = "$Date: 2011-03-15 17:45:23 -0400 (Tue, 15 Mar 2011) $"
__svnId__ = "$Id: test_TemCsvFile.py 2280 2011-03-15 21:45:23Z hdemers $"

# Standard library modules.
import unittest
import logging
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import pySpectrumFileFormat.Edax.TemCsvFile as TemCsvFile
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestTemCsvFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepathRef = Files.getCurrentModulePath(__file__, "../testData/TEM_Edax/OVERALL.CSV")
        if not os.path.isfile(self.filepathRef):
            raise SkipTest

        self.data = TemCsvFile.TemCsvFile(self.filepathRef)

        self.numberPoints = 1024

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_Constructor(self):
        self.assertEquals(self.filepathRef, self.data._filepath)

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_readData(self):
        data = self.data._readData(self.filepathRef)

        channels = data[TemCsvFile.CHANNEL]
        counts = data[TemCsvFile.COUNTS]
        self.assertEquals(self.numberPoints, len(channels))
        self.assertEquals(self.numberPoints, len(counts))

        self.assertEquals(1024, channels[-1])
        self.assertEquals(775, counts[-1])

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

    def test_getData(self):
        energies_eV, counts = self.data.getData()

        self.assertEquals(self.numberPoints, len(energies_eV))
        self.assertEquals(self.numberPoints, len(counts))

        self.assertEquals(10240.0, energies_eV[-1])
        self.assertEquals(775, counts[-1])

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__':    #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
