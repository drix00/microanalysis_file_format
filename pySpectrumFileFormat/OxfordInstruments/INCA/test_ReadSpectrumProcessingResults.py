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
__svnId__ = "$Id: test_ReadSpectrumProcessingResults.py 2280 2011-03-15 21:45:23Z hdemers $"

# Standard library modules.
import unittest
import logging
import os.path

# Third party modules.

# Local modules.
import ReadSpectrumProcessingResults
import DrixUtilities.Files as Files

# Globals and constants variables.

class TestReadSpectrumProcessingResults(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = Files.getCurrentModulePath(__file__, "../../testData/SpectrumProcessing 10.txt")

        self.results = ReadSpectrumProcessingResults.ReadSpectrumProcessingResults(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        results = ReadSpectrumProcessingResults.ReadSpectrumProcessingResults(self.filepath)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_read(self):
        self.results.read(self.filepath)

        data = self.results.data

        self.assertEquals("", data["Element"][1])

        self.assertEquals("Zr", data["Element"][-1])

        self.assertAlmostEquals(-34864.3, data["Area"][1], 1)

        self.assertAlmostEquals(23655.6, data["Area"][-1], 1)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_isValidFile(self):
        folderpath = Files.getCurrentModulePath(__file__, "../../testData")

        filepath = os.path.join(folderpath, "SpectrumFullResults 10.txt")
        self.assertEquals(False, ReadSpectrumProcessingResults.isValidFile(filepath))

        filepath = os.path.join(folderpath, "SpectrumProcessing 10.txt")
        self.assertEquals(True, ReadSpectrumProcessingResults.isValidFile(filepath))

        filepath = os.path.join(folderpath, "AllSpectra.txt")
        self.assertEquals(False, ReadSpectrumProcessingResults.isValidFile(filepath))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
