#!/usr/bin/env python
# -*- coding: utf-8 -*-

# noinspection SpellCheckingInspection
"""
.. py:currentmodule:: microanalysis_file_format.vericold.trace_file
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

TraceFile header
    long    m_dwHeaderSize; //(bytes)
    long    m_dwHeaderVersion;//long

    char    m_lpszDetectorNr[_MAX_PATH];//    format "4"
    char    m_lpszSQUIDNr[_MAX_PATH]; //    format "??"
    char    m_lpszElectronicNr[_MAX_PATH];//format "??"
    char    m_lpszPolarisNr[_MAX_PATH];// format "A1-0000-0-000"

    struct _timeb m_tbFileTime; //abs
    tm        m_tmLocalTime;
    long    m_dwClockTime;    //ms
    long    m_dwLiveTime; //ms
    long    m_dwDeadTime; //ms

    long    m_dwTraceLength;
    double    m_dblSampleRate;

    double    m_dblRegTemperature;
    double    m_dblIBias;
    double    m_dblAmpFactor; //(ADCKarte)
    //must put in VoltsPerBin here 10/4096

    double    m_dblAccVoltage;
    double    m_dblAperture;
    double    m_dblWDistance;
    double    m_dblPixelSize;

Trace header.
        long    m_dwSizeInBytes;//size of this struct - written to file
        //things that change from pulse to pulse
        long    m_dwNumber;         //count number - incremented even if no file open!
        long    m_dwType;         //is the pulse artificial?
        long    m_dwTrigBufPos;     //the trigger position in the DAQ buffer
        __int64 m_i64Time;            //a time stamp in ms since the start of gathering
        double    m_dblTemperature; //from res bridge

        double    m_dblPrePulseLevel; //baseline level before the trigger
        double    m_dblPostPulseLevel;//baseline level after the trigger
        long    m_dwMaxPosition;    //pos the max
        double    m_dblMax;         //value of the max
        long    m_dwMinPosition;    //position of the min
        double    m_dblMin;         //value of the min
        double    m_dblPulseHeight; //the calculated height of the pulse

        //static vars in a run
        double    m_dblSampleRate;    //sample rate
        long    m_dwLength;         //how many samples in the trace
        long    m_dwPreTrigger;     //pos in buff of trigger
        double    m_dblTriggerLevel;    //at what level is the trigger set

        long    m_dwBaseLineLength; //not used
        long    m_dwBaseLineStart;    //not used

    // need some post baseline stuff here
        //these are not yet written to the file
        double    m_dblPostBaseLineLevel;//baseline level after the pulse
        long    m_dwPostBaseLineStart;
        long    m_dwPostBaseLineLength;
        double    m_dblXPos;
        double    m_dblYPos;

Trace data
                //make an array of shorts!!!
                short* pi16Buf = new short[m_dwSize];
                for(int i=0; i<m_dwSize; ++i)
                    pi16Buf[i] = pdblBuf[i];
                gcTraceFile.SaveToFile( pi16Buf,
                                        m_dwSize*sizeof(short));
                delete [] pi16Buf;
"""

###############################################################################
# Copyright 2007 Hendrix Demers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

# Standard library modules.
import os
import time
import struct

# Third party modules.

# Project modules.

# Globals and constants variables.
from microanalysis_file_format.vericold import get_file_size


class TraceFile(object):
    def __init__(self, filename):
        self.headerSize = 1180

        self.headerFormat = "<2i 260s 260s 260s 260s iH2h2x 9i 4i 4x 8d"

        # print "header_format size: %i" % (struct.calcsize(self.header_format))

        self.traceHeaderSize = 148

        self.traceHeaderFormat = "4i ii 3d i d i 3d 2i d 2i d 2i 2d 4x"

        # print "traceHeaderFormat size: %i" % (struct.calcsize("<"+self.traceHeaderFormat))

        self.traceDataSize = 1024*2

        self.traceDataFormat = "1024h"

        # print "traceDataFormat size: %i" % (struct.calcsize("<"+self.traceDataFormat))

        self.traceFormat = "<" + self.traceHeaderFormat + self.traceDataFormat

        # print "traceFormat size: %i" % (struct.calcsize(self.traceFormat))

        self.traceSize = self.traceHeaderSize + self.traceDataSize

        # print "Trace size: %i" % (self.traceSize)

        self.filename = filename

        self.header = {}

    def get_file_size(self):
        return get_file_size(self.filename)

    def print_file_time(self):
        time_last_access = time.localtime(os.stat(self.filename).st_atime)

        time_last_access = time.asctime(time_last_access)

        time_last_modification = time.localtime(os.stat(self.filename).st_mtime)

        time_last_modification = time.asctime(time_last_modification)

        time_last_change = time.localtime(os.stat(self.filename).st_ctime)

        time_last_change = time.asctime(time_last_change)

        print("Time of the last access: {}".format(time_last_access))
        print("Time of the last modification: {}".format(time_last_modification))
        print("Time of the last status change: {}".format(time_last_change))

    def read_trace(self, trace_id):
        if trace_id > 0:  # pragma: no branch
            trace_file = open(self.filename, "rb")

            file_position = self.headerSize + (trace_id - 1) * self.traceSize

            # print trace_id, filePosition

            trace_file.seek(file_position)

            trace_str = trace_file.read(self.traceSize)

            values = struct.unpack(self.traceFormat, trace_str)

            # print len(values)

            # for index,value in enumerate(values):
            #     print "%2i: >>%s<<" % (index, value)

            header = {}

            # Trace header.
            header["SizeInBytes"] = int(values[0])

            # Things that change from pulse to pulse.
            header["TraceID"] = int(values[1])
            header["Type"] = int(values[2])
            header["TrigBufPos"] = int(values[3])
            header["Time"] = int(str(values[4])+str(values[5]))
            header["Temperature"] = float(values[6])

            header["PrePulseLevel"] = float(values[7])
            header["PostPulseLevel"] = float(values[8])
            header["MaxPosition"] = int(values[9])
            header["Max"] = float(values[10])
            header["MinPosition"] = int(values[11])
            header["Min"] = float(values[12])
            header["PulseHeight"] = float(values[13])

            # Static vars in a run.
            header["SampleRate"] = float(values[14])
            header["Length"] = int(values[15])
            header["PreTrigger"] = int(values[16])
            header["TriggerLevel"] = float(values[17])

            # Not used.
            header["BaseLineLength"] = int(values[18])
            header["BaseLineStart"] = int(values[19])

            # Need some post baseline stuff here.
            # These are not yet written to the file
            header["PostBaseLineLevel"] = float(values[20])
            header["PostBaseLineStart"] = int(values[21])
            header["PostBaseLineLength"] = int(values[22])
            header["XPos"] = float(values[23])
            header["YPos"] = float(values[24])

            data = []

            for index in range(25, 1025, 1):
                data.append(float(values[index]))

            # header_keys = sorted(header.keys())
            # for key in headerKeys:
            #     print "%s: >>%s<<" % (key, header[key])

            time_step_ms = 1.0E3 / header["SampleRate"]

            times_ms = []
            for index, dummy_value in enumerate(data):
                time_ms = time_step_ms * index

                times_ms.append(time_ms)

                # print "%0.4f\t%0.4f" % (time_ms, value)

            return header, times_ms, data

    # noinspection SpellCheckingInspection
    def read_header(self):
        trace_file = open(self.filename, "rb")

        header_str = trace_file.read(self.headerSize)

        values = struct.unpack(self.headerFormat, header_str)

        # print len(values)

        # for index,value in enumerate(values):
        #     print "%2i: >>%s<<" % (index, value)

        self.header["Size"] = int(values[0])

        self.header["Version"] = int(values[1])

        self.header["DetectorNumber"] = values[2]

        self.header["SQUIDNumber"] = values[3]

        self.header["ElectronicNumber"] = values[4]

        self.header["PolarisNumber"] = values[5]

        self.header["CurrentSystemTime_64"] = str(values[6]) + str(values[7])

        self.header["CurrentSystemTime_milli"] = int(values[7])

        self.header["CurrentSystemTime_timezone"] = int(values[8])

        self.header["CurrentSystemTime_dstflag"] = int(values[9])

        self.header["Localtime_sec"] = int(values[10])
        self.header["Localtime_min"] = int(values[11])
        self.header["Localtime_hour"] = int(values[12])
        self.header["Localtime_mday"] = int(values[13])
        self.header["Localtime_mon"] = int(values[14])
        self.header["Localtime_year"] = int(values[15])
        self.header["Localtime_wday"] = int(values[16])
        self.header["Localtime_yday"] = int(values[17])
        self.header["Localtime_isdst"] = int(values[18])

        self.header["ClockTime_ms"] = int(values[19])
        self.header["LiveTime_ms"] = int(values[20])
        self.header["DeadTime_ms"] = int(values[21])

        self.header["TraceLength"] = int(values[22])
        self.header["SampleRate"] = float(values[23])

        self.header["RegTemperature"] = float(values[24])
        self.header["IBias"] = float(values[25])
        self.header["AmpFactor"] = float(values[26])

        self.header["AccVoltage"] = float(values[27])
        self.header["Aperture"] = float(values[28])
        self.header["WDistance"] = float(values[29])
        self.header["PixelSize"] = float(values[30])

    # noinspection SpellCheckingInspection
    def print_header(self):
        print("Size: ", self.header["Size"])
        print("Version: ", self.header["Version"])

        # print("DetectorNumber: >>%s<<" % self.header["DetectorNumber"])
        # print("SQUIDNumber: >>%s<<" % self.header["SQUIDNumber"])
        # print("ElectronicNumber: >>%s<<" % self.header["ElectronicNumber"])
        # print("PolarisNumber: >>%s<<" % self.header["PolarisNumber"])

        print("CurrentSystemTime_64", self.header["CurrentSystemTime_64"])
        print("CurrentSystemTime_milli", self.header["CurrentSystemTime_milli"])
        print("CurrentSystemTime_timezone", self.header["CurrentSystemTime_timezone"])
        print("CurrentSystemTime_dstflag", self.header["CurrentSystemTime_dstflag"])

        print("Localtime_sec", self.header["Localtime_sec"])
        print("Localtime_min", self.header["Localtime_min"])
        print("Localtime_hour", self.header["Localtime_hour"])
        print("Localtime_mday", self.header["Localtime_mday"])
        print("Localtime_mon", self.header["Localtime_mon"])
        print("Localtime_year", self.header["Localtime_year"])
        print("Localtime_wday", self.header["Localtime_wday"])
        print("Localtime_yday", self.header["Localtime_yday"])
        print("Localtime_isdst", self.header["Localtime_isdst"])

        print("ClockTime_ms", self.header["ClockTime_ms"])
        print("LiveTime_ms", self.header["LiveTime_ms"])
        print("DeadTime_ms", self.header["DeadTime_ms"])

        print("TraceLength", self.header["TraceLength"])
        print("SampleRate", self.header["SampleRate"])

        print("RegTemperature", self.header["RegTemperature"])
        print("IBias", self.header["IBias"])
        print("AmpFactor", self.header["AmpFactor"])

        print("AccVoltage", self.header["AccVoltage"])
        print("Aperture", self.header["Aperture"])
        print("WDistance", self.header["WDistance"])
        print("PixelSize", self.header["PixelSize"])

    def get_pulse(self, pulse_id, gain=1.0 / 5.0E3):
        dummy_header, times_ms, data = self.read_trace(pulse_id)

        baseline = compute_baseline(times_ms, data)

        pulse_data = [(xx - baseline)*gain for xx in data]

        return times_ms, pulse_data


def compute_baseline(times_ms, data):
    end_index = 0

    for index, time_ms in enumerate(times_ms):  # pragma: no branch
        if time_ms >= 0.2:
            end_index = index
            break

    total = sum(data[:end_index])
    number = len(data[:end_index])

    baseline = total/number

    return baseline
