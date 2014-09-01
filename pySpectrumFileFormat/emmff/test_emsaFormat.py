#!/usr/bin/env python

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2007 Hendrix Demers"
__license__ = ""

# Subversion informations for the file.
__svnRevision__ = "$Revision: 2917 $"
__svnDate__ = "$Date: 2013-10-13 21:11:56 -0400 (Sun, 13 Oct 2013) $"
__svnId__ = "$Id: test_emsaFormat.py 2917 2013-10-14 01:11:56Z hdemers $"

import unittest
import logging
import sys

import emsaFormat
import DrixUtilities.Files as Files

class emsaFormatTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.filepath = Files.getCurrentModulePath(__file__, "../emmff/spectra/spectrum1.emsa")

        self.emsa = emsaFormat.EmsaFormat(self.filepath)

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testConstructor(self):
        emsaFormat.EmsaFormat()

    def testReadFile(self):
        filename = Files.getCurrentModulePath(__file__, "../emmff/spectra/spectrum1.emsa")

        self.emsa.open(filename)

        self.assertNotEqual(0, len(self.emsa.lines))

        self.assertEqual(1054, len(self.emsa.lines))

        filename = Files.getCurrentModulePath(__file__, "../emmff/spectra/BadFile.emsa")

        self.assertRaises(IOError, self.emsa.open, filename)

    def testIsLineData(self):
        line = ""
        self.assertEqual(False, self.emsa.isLineData(line)[0], msg="Empty line")
        self.assertEqual(None, self.emsa.isLineData(line)[1], msg="Empty line")
        self.assertEqual(0, self.emsa.isLineData(line)[2], msg="Empty line")

        line = None
        self.assertEqual(False, self.emsa.isLineData(line)[0], msg="None line")
        self.assertEqual(None, self.emsa.isLineData(line)[1], msg="None line")
        self.assertEqual(0, self.emsa.isLineData(line)[2], msg="None line")

        self.emsa = emsaFormat.EmsaFormat()
        line = "1.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="Y value")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="Y value")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="Y value")

        line = "1.2, 0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With comma")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With comma")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With comma")

        line = "1.2 0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With space")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With space")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With space")

        line = "1.2\t0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With tab")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With tab")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With tab")

        line = "0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 1 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 1 column")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With 1 column")

        line = "0.1, 0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 2 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 2 column")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With 2 column")

        line = "0.1, 0.2, 0.3"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 3 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 3 column")
        self.assertEqual(3, self.emsa.isLineData(line)[2], msg="With 3 column")

        line = "0.1, 0.2, 0.3, 0.4"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 4 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 4 column")
        self.assertEqual(4, self.emsa.isLineData(line)[2], msg="With 4 column")

        line = "0.1, 0.2, 0.3, 0.4, 0.5"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 5 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 5 column")
        self.assertEqual(5, self.emsa.isLineData(line)[2], msg="With 5 column")

        line = "0.1, 0.2, 0.3, 0.4, 0.5, 0.6"
        self.assertEqual(False, self.emsa.isLineData(line)[0], msg="With 6 column")
        self.assertEqual(None, self.emsa.isLineData(line)[1], msg="With 6 column")
        self.assertEqual(0, self.emsa.isLineData(line)[2], msg="With 6 column")

        line = "0.1 0.2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 2 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 2 column")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With 2 column")

        line = "0.1 0.2 0.3"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 3 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 3 column")
        self.assertEqual(3, self.emsa.isLineData(line)[2], msg="With 3 column")

        line = "0.1 0.2 0.3 0.4"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 4 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 4 column")
        self.assertEqual(4, self.emsa.isLineData(line)[2], msg="With 4 column")

        line = "0.1 0.2 0.3 0.4 0.5"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With 5 column")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With 5 column")
        self.assertEqual(5, self.emsa.isLineData(line)[2], msg="With 5 column")

        line = "0.1 0.2 0.3 0.4 0.5 0.6"
        self.assertEqual(False, self.emsa.isLineData(line)[0], msg="With 6 column")
        self.assertEqual(None, self.emsa.isLineData(line)[1], msg="With 6 column")
        self.assertEqual(0, self.emsa.isLineData(line)[2], msg="With 6 column")

        line = "2"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With integer")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With integer")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With integer")

        line = ".1"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="Without leading zero")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="Without leading zero")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="Without leading zero")

        line = "1.0E-6"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With scinetific notation")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With scinetific notation")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With scinetific notation")

        line = "1.0e6"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With scinetific notation")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With scinetific notation")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With scinetific notation")

        line = "1.0d6"
        if sys.platform == 'win32' and "32 bit" in sys.version:
            self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With bad character")
            self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With bad character")
            self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With bad character")
        elif sys.platform == 'win32' and "64 bit" in sys.version:
            self.assertEqual(False, self.emsa.isLineData(line)[0], msg="With bad character")
            self.assertEqual(None, self.emsa.isLineData(line)[1], msg="With bad character")
            self.assertEqual(0, self.emsa.isLineData(line)[2], msg="With bad character")
        else:
            self.assertEqual(False, self.emsa.isLineData(line)[0], msg="With bad character")
            self.assertEqual(None, self.emsa.isLineData(line)[1], msg="With bad character")
            self.assertEqual(0, self.emsa.isLineData(line)[2], msg="With bad character")

        line = "#1.0"
        self.assertEqual(False, self.emsa.isLineData(line)[0], msg="With leading #")
        self.assertEqual(None, self.emsa.isLineData(line)[1], msg="With leading #")
        self.assertEqual(0, self.emsa.isLineData(line)[2], msg="With leading #")

        line = "    0.1"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With leading space")
        self.assertEqual('Y', self.emsa.isLineData(line)[1], msg="With leading space")
        self.assertEqual(1, self.emsa.isLineData(line)[2], msg="With leading space")

        line = "         0.0000,             0.0,"
        self.assertEqual(True, self.emsa.isLineData(line)[0], msg="With leading space")
        self.assertEqual('XY', self.emsa.isLineData(line)[1], msg="With leading space")
        self.assertEqual(2, self.emsa.isLineData(line)[2], msg="With leading space")

    def testIsLineKeyword(self):
        line = ""
        self.assertEqual(False, self.emsa.isLineKeyword(line), msg="Empty line")

        line = None
        self.assertEqual(False, self.emsa.isLineKeyword(line), msg="None line")

        line = "#keyword"
        self.assertEqual(True, self.emsa.isLineKeyword(line), msg="With leading #")

        line = "    #keyword"
        self.assertEqual(True, self.emsa.isLineKeyword(line), msg="With leading space + #")

        line = "\t#keyword"
        self.assertEqual(True, self.emsa.isLineKeyword(line), msg="With leading space + #")

        line = "1#keyword"
        self.assertEqual(False, self.emsa.isLineKeyword(line), msg="With invalid line")

        line = "1.2, 0.2"
        self.assertEqual(False, self.emsa.isLineKeyword(line), msg="With invalid line")

        line = "1.2 0.2"
        self.assertEqual(False, self.emsa.isLineKeyword(line), msg="With invalid line")

    def testReadKeywordLine(self):
        line = r"#FORMAT      : EMSA/MAS Spectral Data File"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("FORMAT", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("EMSA/MAS Spectral Data File", data)

        line = r"#VERSION     : 1.0"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("VERSION", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("1.0", data)

        line = r"#TITLE       : Spectrum 1"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("TITLE", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("Spectrum 1", data)

        line = r"#DATE        : 20-NOV-2006"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("DATE", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("20-NOV-2006", data)

        line = r"#TIME        : 16:03"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("TIME", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("16:03", data)

        line = r"#XPOSITION mm: 0.0000"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("XPOSITION", keyword)
        self.assertEquals("mm", keywordComment)
        self.assertEquals("0.0000", data)

        line = r"##OXINSTELEMS: 6,8,12"
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals("OXINSTELEMS", keyword)
        self.assertEquals("", keywordComment)
        self.assertEquals("6,8,12", data)

        line = r"-0.200, 0."
        keyword, keywordComment, data = self.emsa.readKeywordLine(line)
        self.assertEquals(None, keyword)
        self.assertEquals(None, keywordComment)
        self.assertEquals(None, data)

    def testReadDataLine(self):
        line = r"-0.200, 0."
        values = self.emsa.readDataLine(line)
        self.assertEquals(2, len(values))
        self.assertEquals(-0.2, values[0])
        self.assertEquals(0.0, values[1])

        line = r"-0.200 0."
        values = self.emsa.readDataLine(line)
        self.assertEquals(2, len(values))
        self.assertEquals(-0.2, values[0])
        self.assertEquals(0.0, values[1])

        line = r"-0.200"
        values = self.emsa.readDataLine(line)
        self.assertEquals(1, len(values))
        self.assertEquals(-0.2, values[0])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0"
        values = self.emsa.readDataLine(line)
        self.assertEquals(5, len(values))
        self.assertEquals(1.0, values[0])
        self.assertEquals(5.0, values[-1])

        line = r"1.0, 2.0, 3.0, 4.0, 5.0, 6.0"
        values = self.emsa.readDataLine(line)
        self.assertEquals(6, len(values))
        self.assertEquals(1.0, values[0])
        self.assertEquals(6.0, values[-1])

        line = r"#VERSION         : 1.0"
        values = self.emsa.readDataLine(line)
        self.assertEquals(None, values)

    def testReadLine(self):
        emsa = emsaFormat.EmsaFormat()

        line = r"-0.200, 0."
        emsa.readLine(line)
        self.assertEquals(1, len(emsa.values))
        self.assertEquals(-0.2, emsa.values[0][0])
        self.assertEquals(0.0, emsa.values[0][1])

        line = r"#FORMAT            : EMSA/MAS Spectral Data File"
        emsa.readLine(line)
        self.assertEquals(1, len(emsa.keywords))
        self.assertEquals("FORMAT", emsa.keywords[0]["keyword"])
        self.assertEquals(1, emsa.keywords[0]["order"])

        line = r"#VERSION         : 1.0"
        emsa.readLine(line)
        self.assertEquals(2, len(emsa.keywords))
        self.assertEquals("VERSION", emsa.keywords[1]["keyword"])
        self.assertEquals(2, emsa.keywords[1]["order"])

        line = r"#TITLE             : Spectrum 1"
        emsa.readLine(line)
        self.assertEquals(3, len(emsa.keywords))
        self.assertEquals("TITLE", emsa.keywords[2]["keyword"])
        self.assertEquals(3, emsa.keywords[2]["order"])

    def testReadlines(self):
        emsa = emsaFormat.EmsaFormat()

        filename = Files.getCurrentModulePath(__file__, "../emmff/spectra/spectrum1.emsa")

        emsa.open(filename)

        emsa.readLines()

        self.assertEquals(30, len(emsa.keywords))

        self.assertEquals(1024, len(emsa.values))

    def testSetGetFormat(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getFormat())

        self.assertEquals("EMSA/MAS Spectral Data File", self.emsa.getFormat())

    def testIsFileValid(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.isFileValid)

        self.assertEquals(True, self.emsa.isFileValid)

    def testSetGetVersion(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getVersion())

        self.assertEquals("1.0", self.emsa.getVersion())

    def testSetGetTitle(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getTitle())

        self.assertEquals("Spectrum 1", self.emsa.getTitle())

    def testSetGetDate(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getDate())

        self.assertEquals("20-NOV-2006", self.emsa.getDate())

    def testSetGetTime(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getTime())

        self.assertEquals("16:03", self.emsa.getTime())

    def testSetGetOwner(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getOwner())

        self.assertEquals("helen", self.emsa.getOwner())

    def testSetGetNumberPoints(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getNumberPoints())

        self.assertEquals(1024.0, self.emsa.getNumberPoints())

    def testSetGetNumberColumns(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getNumberColumns())

        self.assertEquals(1.0, self.emsa.getNumberColumns())

    def testSetGetXUnits(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getXUnits())

        self.assertEquals("keV", self.emsa.getXUnits())

    def testSetGetYUnits(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getYUnits())

        self.assertEquals("counts", self.emsa.getYUnits())

    def testSetGetDataType(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getDataType())

        self.assertEquals("XY", self.emsa.getDataType())

    def testSetGetXPerChannel(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getXPerChannel())

        self.assertEquals(0.02, self.emsa.getXPerChannel())

    def testSetGetOffset(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getOffset())

        self.assertEquals(-0.2, self.emsa.getOffset())

    def testSetGetSignalType(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getSignalType())

        self.assertEquals("EDS", self.emsa.getSignalType())

    def testSetGetChannelOffset(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getChannelOffset())

        self.assertEquals(10.0, self.emsa.getChannelOffset())

    def testSetGetLiveTime(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getLiveTime())

        self.assertEquals(0.34635, self.emsa.getLiveTime())

    def testSetGetRealTime(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getRealTime())

        self.assertEquals(0.453241, self.emsa.getRealTime())

    def testSetGetBeamEnergy(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getBeamEnergy())

        self.assertEquals(5.0, self.emsa.getBeamEnergy())

    def testSetGetProbeCurrent(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getProbeCurrent())

        self.assertEquals(0.0, self.emsa.getProbeCurrent())

    def testSetGetMagnification(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getMagnification())

        self.assertEquals(250.0, self.emsa.getMagnification())

    def testSetGetXPosition(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getXPosition())

        self.assertEquals(0.0, self.emsa.getXPosition())

    def testSetGetYPosition(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getYPosition())

        self.assertEquals(0.0, self.emsa.getYPosition())

    def testSetGetZPosition(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getZPosition())

        self.assertEquals(0.0, self.emsa.getZPosition())

    def testSetGetOxfordInstrumentsElement(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getOxfordInstrumentsElement())

        self.assertEquals("6,8,12", self.emsa.getOxfordInstrumentsElement())

    def testSetGetOxfordInstrumentsLabel(self):
        emsa = emsaFormat.EmsaFormat()
        self.assertEquals(None, emsa.getOxfordInstrumentsLabel())

        self.assertEquals("8, 0.525, O", self.emsa.getOxfordInstrumentsLabel())

    def testCreateXData(self):
        xData = self.emsa.createXData(1024, -0.2, 0.02)
        self.assertEquals(1024, len(xData))

        xDataRef = self.emsa.getDataX()
        self.assertEquals(1024, len(xDataRef))

        self.assertAlmostEquals(xDataRef[0], xData[0])
        self.assertAlmostEquals(xDataRef[10], xData[10])
        self.assertAlmostEquals(xDataRef[-1], xData[-1])
        self.assertAlmostEquals(xDataRef[-10], xData[-10])

    def testReadFileTEMBruker(self):
        filename = Files.getCurrentModulePath(__file__, "../testData/TEM_Bruker/Gold-pt 2-2.msa")

        emsa = emsaFormat.EmsaFormat()
        emsa.open(filename)
        emsa.readLines()
        emsa.setHeader()
        emsa.setSpectrumData()

        self.assertNotEqual(0, len(emsa.lines))

        self.assertEqual(1055, len(emsa.lines))

        self.assertEqual(1024, len(emsa.values))
        self.assertEqual(3072, len(emsa.getDataX()))
        self.assertEqual(3072, len(emsa.getDataY()))

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()
