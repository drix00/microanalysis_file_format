#!/usr/bin/env python
""" """

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2282 $"
__svnDate__ = "$Date: 2011-03-15 17:46:04 -0400 (Tue, 15 Mar 2011) $"
__svnId__ = "$Id: test_genesisPolarisFile.py 2282 2011-03-15 21:46:04Z hdemers $"

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
import genesisPolarisFile
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestgenesisPolarisFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = Files.getCurrentModulePath(__file__, "../testData/k3670_30keV_OFeCalibration.csp")

        self.gpFile = genesisPolarisFile.GenesisPolarisFile()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        gpFile = genesisPolarisFile.GenesisPolarisFile()

        self.assertEquals(False, gpFile.isFileRead)

        gpFile = genesisPolarisFile.GenesisPolarisFile(self.filepath)

        self.assertEquals(True, gpFile.isFileRead)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_readFile(self):
        self.assertEquals(False, self.gpFile.isFileRead)

        self.gpFile.readFile(self.filepath)

        self.assertEquals(True, self.gpFile.isFileRead)

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def test_readHeader(self):
        header = self.gpFile.readHeader(self.filepath)

        self.assertEquals(1001, header["version"])

        self.assertEquals(3072, header["pixOffset"])

        self.assertEquals(0, header["pixSize"])

        self.assertEquals(3072, header["dataOffset"])

        self.assertEquals(19724, header["dataSize"])

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
