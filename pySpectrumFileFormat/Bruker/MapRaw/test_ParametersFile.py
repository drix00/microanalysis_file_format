#!/usr/bin/env python
"""
.. py:currentmodule:: OxfordInstruments.MapRaw.test_ParametersFile
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

description
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
import os.path

# Third party modules.
from nose.plugins.skip import SkipTest

# Local modules.
import pyHendrixDemersTools.Files as Files

# Project modules
import pySpectrumFileFormat.Bruker.MapRaw.ParametersFile as ParametersFile

# Globals and constants variables.

class TestParametersFile(unittest.TestCase):
    """
    TestCase class for the module `ParametersFile`.
    """

    def setUp(self):
        """
        Setup method.
        """

        unittest.TestCase.setUp(self)

        self.path = Files.getCurrentModulePath(__file__, "../../../testData/Bruker/MapRaw")

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

    def test_read(self):
        filename = "Sample01.rpl"
        filepath = os.path.join(self.path, filename)
        if not os.path.isfile(filepath):
            raise SkipTest

        parameters = ParametersFile.ParametersFile()
        parameters.read(filepath)

        self.assertEquals(1024, parameters.width)
        self.assertEquals(768, parameters.height)
        self.assertEquals(2048, parameters.depth)
        self.assertEquals(0, parameters.offset)
        self.assertEquals(1, parameters.dataLength_B)
        self.assertEquals(ParametersFile.DATA_TYPE_UNSIGNED, parameters.dataType)
        self.assertEquals(ParametersFile.BYTE_ORDER_DONT_CARE, parameters.byteOrder)
        self.assertEquals("vector", parameters.recordBy)

        #self.fail("Test if the testcase is working.")

if __name__ == '__main__':  #pragma: no cover
    import nose
    import sys
    argv = sys.argv
    argv.append("--cover-package=pySpectrumFileFormat.Bruker.MapRaw.ParametersFile")
    nose.runmodule(argv=argv)
