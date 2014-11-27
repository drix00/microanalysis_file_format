#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2280 $"
__svnDate__ = "$Date: 2011-03-15 17:45:23 -0400 (Tue, 15 Mar 2011) $"
__svnId__ = "$Id: test_ReadAllSpectrumResults.py 2280 2011-03-15 21:45:23Z hdemers $"

# Standard library modules.
import unittest
import logging
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import pySpectrumFileFormat.OxfordInstruments.INCA.ReadAllSpectrumResults as ReadAllSpectrumResults
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestReadAllSpectrumResults(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = Files.getCurrentModulePath(__file__, "../../testData/AllSpectra.txt")
        if not os.path.isfile(self.filepath):
            raise SkipTest

        self.results = ReadAllSpectrumResults.ReadAllSpectrumResults(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        results = ReadAllSpectrumResults.ReadAllSpectrumResults(self.filepath)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_read(self):
        self.results.read(self.filepath)

        data = self.results.data

        self.assertAlmostEquals(0.853, data["Spectrum 5"][1], 3)

        self.assertAlmostEquals(100.000, data["Spectrum 5"][-1], 3)

        self.assertAlmostEquals(0.520, data["Minimum"][1], 3)

        self.assertAlmostEquals(15.128, data["Minimum"][-1], 3)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_extractMinData(self):
        #line = "Min.    19.086    0.520    4.404    0.598    40.670    14.894    15.128     "
        line = "Min.\t19.086\t0.520\t4.404\t0.598\t40.670\t14.894\t15.128\t"
        results = self.results._extractLineData(line)

        self.assertAlmostEquals(0.520, results[1], 3)

        self.assertAlmostEquals(15.128, results[-1], 3)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_isValidFile(self):
        folderpath = Files.getCurrentModulePath(__file__, "../../testData")

        filepath = os.path.join(folderpath, "SpectrumFullResults 10.txt")
        self.assertEquals(False, ReadAllSpectrumResults.isValidFile(filepath))

        filepath = os.path.join(folderpath, "SpectrumProcessing 10.txt")
        self.assertEquals(False, ReadAllSpectrumResults.isValidFile(filepath))

        filepath = os.path.join(folderpath, "AllSpectra.txt")
        self.assertEquals(True, ReadAllSpectrumResults.isValidFile(filepath))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
