#!/usr/bin/env python
"""
.. py:currentmodule:: OxfordInstruments.MapRaw.MapRawFormat
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read Oxford Instruments map in the raw format.
"""

# Script information for the file.
__author__ = "Hendrix Demers (hendrix.demers@mail.mcgill.ca)"
__version__ = ""
__date__ = ""
__copyright__ = "Copyright (c) 2012 Hendrix Demers"
__license__ = ""

# Standard library modules.
import os.path
import struct
import logging

# Third party modules.
import matplotlib.pyplot as plt
import numpy as np

# Local modules.

# Project modules
import pySpectrumFileFormat.OxfordInstruments.MapRaw.ParametersFile as ParametersFile

# Globals and constants variables.

class MapRawFormat(object):
    def __init__(self, rawFilepath):
        logging.info("Raw file: %s", rawFilepath)

        self._rawFilepath = rawFilepath
        parametersFilepath = self._rawFilepath.replace('.raw', '.rpl')

        self._parameters = ParametersFile.ParametersFile()
        self._parameters.read(parametersFilepath)

        self._format = self._generateFormat(self._parameters)

    def _generateFormat(self, parameters):
        spectrumFormat = ""
        if parameters.byteOrder == ParametersFile.BYTE_ORDER_LITTLE_ENDIAN:
            spectrumFormat += '<'

        if parameters.dataLength_B == 1:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "b"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "B"
        elif parameters.dataLength_B == 2:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "h"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "H"
        elif parameters.dataLength_B == 4:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "i"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "I"

        logging.info("Format: %s", spectrumFormat)

        return spectrumFormat

    def _generateSumSpectraFormat(self, parameters):
        spectrumFormat = ""
        if parameters.byteOrder == ParametersFile.BYTE_ORDER_LITTLE_ENDIAN:
            spectrumFormat += '<'

        spectrumFormat += '%i' % (parameters.width*parameters.height)

        if parameters.dataLength_B == 1:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "b"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "B"
        elif parameters.dataLength_B == 2:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "h"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "H"
        elif parameters.dataLength_B == 4:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "i"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "I"

        logging.info("Format: %s", spectrumFormat)

        return spectrumFormat

    def _generateSpectraFormatVector(self, parameters):
        spectrumFormat = ""
        if parameters.byteOrder == ParametersFile.BYTE_ORDER_LITTLE_ENDIAN:
            spectrumFormat += '<'

        spectrumFormat += '%i' % (parameters.depth)

        if parameters.dataLength_B == 1:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "b"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "B"
        elif parameters.dataLength_B == 2:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "h"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "H"
        elif parameters.dataLength_B == 4:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "i"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "I"

        logging.debug("Format: %s", spectrumFormat)

        return spectrumFormat

    def _generateSumSpectraFormatVector(self, parameters):
        spectrumFormat = ""
        if parameters.byteOrder == ParametersFile.BYTE_ORDER_LITTLE_ENDIAN:
            spectrumFormat += '<'

        numberPixels = parameters.width*parameters.height

        spectrumFormat += '%i' % (parameters.depth*numberPixels)

        if parameters.dataLength_B == 1:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "b"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "B"
        elif parameters.dataLength_B == 2:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "h"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "H"
        elif parameters.dataLength_B == 4:
            if parameters.dataType == ParametersFile.DATA_TYPE_SIGNED:
                spectrumFormat += "i"
            elif parameters.dataType == ParametersFile.DATA_TYPE_UNSIGNED:
                spectrumFormat += "I"

        logging.debug("Format: %s", spectrumFormat)

        return spectrumFormat

    def getSpectrum(self, pixelId):
        logging.debug("Pixel ID: %i", pixelId)

        imageOffset = self._parameters.width*self._parameters.height
        logging.debug("File offset: %i", imageOffset)

        logging.debug("Size: %i", struct.calcsize(self._format))

        if self._parameters.recordBy == ParametersFile.RECORED_BY_IMAGE:
            x = np.arange(0, self._parameters.depth)
            y = np.zeros_like(x)
            rawFile = open(self._rawFilepath, 'rb')
            for channel in range(self._parameters.depth):
                fileOffset = self._parameters.offset + (pixelId + channel*imageOffset)*self._parameters.dataLength_B
                rawFile.seek(fileOffset)
                fileBuffer = rawFile.read(struct.calcsize(self._format))
                items = struct.unpack(self._format, fileBuffer)
                y[channel] = float(items[0])

            rawFile.close()
        elif self._parameters.recordBy == ParametersFile.RECORED_BY_VECTOR:
            spectrumFormat = self._generateSpectraFormatVector(self._parameters)

            x = np.arange(0, self._parameters.depth)
            y = np.zeros_like(x)
            rawFile = open(self._rawFilepath, 'rb')

            fileOffset = self._parameters.offset + pixelId*self._parameters.dataLength_B
            rawFile.seek(fileOffset)
            fileBuffer = rawFile.read(struct.calcsize(spectrumFormat))
            items = struct.unpack(spectrumFormat, fileBuffer)
            y = np.array(items)

            rawFile.close()

            assert len(x) == len(y)
        return x, y

    def getSumSpectrum(self):
        imageOffset = self._parameters.width*self._parameters.height
        x = np.arange(0, self._parameters.depth)
        y = np.zeros_like(x)
        rawFile = open(self._rawFilepath, 'rb')
        fileOffset = self._parameters.offset
        rawFile.seek(fileOffset)

        if self._parameters.recordBy == ParametersFile.RECORED_BY_IMAGE:
            sumSpectrumformat = self._generateSumSpectraFormat(self._parameters)
            for channel in range(self._parameters.depth):
                logging.info("Channel: %i", channel)
                fileBuffer = rawFile.read(struct.calcsize(sumSpectrumformat))
                items = struct.unpack(sumSpectrumformat, fileBuffer)
                y[channel] = np.sum(items)

        elif self._parameters.recordBy == ParametersFile.RECORED_BY_VECTOR:
            sumSpectrumformat = self._generateSumSpectraFormatVector(self._parameters)
            fileBuffer = rawFile.read(struct.calcsize(sumSpectrumformat))
            items = struct.unpack(sumSpectrumformat, fileBuffer)
            data = np.array(items)
            data = data.reshape(self._parameters.width, self._parameters.height, self._parameters.depth)
            y = data.sum(axis=(0, 1))

        rawFile.close()

        assert len(x) == len(y)
        return x, y

    def getSumSpectrumOld(self):
        numberPixels = self._parameters.width*self._parameters.height
        logging.info("Numbe rof pixels: %i", numberPixels)

        x = np.arange(0, self._parameters.depth)
        ySum = np.zeros_like(x)

        for pixelId in range(numberPixels):
            _x, y = self.getSpectrum(pixelId)
            ySum += y

        return x, ySum

def run():
    path = r"J:\hdemers\work\mcgill2012\results\experimental\McGill\su8000\others\exampleEDS"
    #filename = "Map30kV.raw"
    filename = "Project 1.raw"
    filepath = os.path.join(path, filename)

    mapRaw = MapRawFormat(filepath)

    line = 150
    column = 150
    pixelId = line + column*512
    xData, yData = mapRaw.getSpectrum(pixelId=pixelId)

    plt.figure()
    plt.plot(xData, yData)

    xData, yData = mapRaw.getSumSpectrum()

    plt.figure()
    plt.plot(xData, yData)
    plt.show()

def run20120307():
    path = r"J:\hdemers\work\mcgill2012\results\experimental\McGill\su8000\hdemers\20120307\rareearthSample"
    filename = "mapSOI_15.raw"
    filepath = os.path.join(path, filename)

    mapRaw = MapRawFormat(filepath)

    line = 150
    column = 150
    pixelId = line + column*512
    xData, yData = mapRaw.getSpectrum(pixelId=pixelId)

    plt.figure()
    plt.plot(xData, yData)
    plt.show()

if __name__ == '__main__': #pragma: no cover
    import pyHendrixDemersTools.Runner as Runner
    Runner.Runner().run(runFunction=run)
