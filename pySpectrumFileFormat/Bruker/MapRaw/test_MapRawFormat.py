#!/usr/bin/env python
"""
.. py:currentmodule:: OxfordInstruments.MapRaw.test_MapRawFormat
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Tests for module `MapRawFormat`.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.

# Project modules
import pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat as MapRawFormat

# Globals and constants variables.

class TestMapRawFormat(unittest.TestCase):
    """
    TestCase class for the module `MapRawFormat`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

    def tearDown(self):
        """
        Teardown method.
        """

        unittest.TestCase.tearDown(self)

    def testSkeleton(self):
        """
        First test to check if the testcase is working with the testing framework.
        """

        #self.fail("Test if the testcase is working.")
        self.assert_(True)

if __name__ == '__main__':  #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=pySpectrumFileFormat.Bruker.MapRaw.MapRawFormat")
    nose.runmodule(argv=argv)
