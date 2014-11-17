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
__svnId__ = "$Id: test_TraceFile.py 2280 2011-03-15 21:45:23Z hdemers $"

# Standard library modules.
import unittest
import logging
import os.path

# Third party modules.

# Local modules.
import TraceFile
import pyHendrixDemersTools.Files as Files

# Globals and constants variables.

class TestTraceFile(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = Files.getCurrentModulePath(__file__, "../testData/test01.trc")

        self.traceFile = TraceFile.TraceFile(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testConstructor(self):
        traceFile = TraceFile.TraceFile(self.filepath)

        self.assertTrue(os.path.isfile(traceFile.filename))

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

    def testGetFileSize(self):
        self.assertEquals(3253456, self.traceFile.getFileSize())

        #self.traceFile.printFileTime()

        #self.fail("Test if the TestCase is working.")
        self.assertTrue(True)

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
