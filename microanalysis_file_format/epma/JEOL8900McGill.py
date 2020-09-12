#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.epma.JEOL8900McGill
.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Read the McGill JEOL 8900 epma data.
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
import warnings

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


class DataPoint:
    def __init__(self):
        self.spectrum_id = 0
        self.element_data = {}
        self.group = None
        self.sample = None
        self.number = 0
        self.comment = ""
        self.stage_x = 0.0
        self.stage_y = 0.0
        self.stage_z = 0.0
        self.incident_energy_keV = 0.0
        self.probe_diameter = 0.0
        self.scan_on = False
        self.date = None
        self.detector_type = None
        self.number_accumulation = 0
        self.current_A = 0.0

    @staticmethod
    def read_id_line(line):
        start = len('Unknown Specimen No.')

        specimen_id = int(line[start:])

        return specimen_id

    @staticmethod
    def read_group_sample_line(line):
        group = line[16:32].strip()

        sample = line[42:].strip()

        return group, sample

    @staticmethod
    def read_number_comment_line(line):
        number = int(line[16:32].strip())

        comment = line[42:].strip()

        return number, comment

    @staticmethod
    def read_stage_line(line):
        stage_x = float(line[22:33].strip())

        stage_y = float(line[36:47].strip())

        stage_z = float(line[50:].strip())

        return stage_x, stage_y, stage_z

    @staticmethod
    def read_beam_line(line):
        incident_energy_keV = float(line[16:24].strip())

        probe_diameter = float(line[45:50].strip())

        scan_on = line[57:].strip()

        if scan_on == 'Off':
            scan_on = False
        else:
            scan_on = True

        return incident_energy_keV, probe_diameter, scan_on

    @staticmethod
    def read_date_line(line):
        start = len(' Dated on')

        date = line[start:].strip()

        return date

    @staticmethod
    def read_detector_line(line):
        detector_type = line[:16].strip()

        number_accumulation = int(line[38:].strip())

        return detector_type, number_accumulation

    @staticmethod
    def read_current_line(line):
        current_A = float(line[11:].strip())

        return current_A

    @staticmethod
    def get_positions(lines):
        positions = {}

        for line in lines:
            if 'Element Peak(mm)' in line:
                index = lines.index(line)
                positions['intensity'] = (index+1, 0)

            if 'Element  f(chi)' in line:
                index = lines.index(line)
                positions['correction'] = (index+1, 0)
                positions['intensity'] = (positions['intensity'][0], index)

            if 'Element  El. Wt%' in line:
                index = lines.index(line)
                positions['concentration'] = (index+1, 0)
                positions['correction'] = (positions['correction'][0], index)

            if 'Total:' in line:
                index = lines.index(line)
                positions['total'] = (index, index+1)
                positions['concentration'] = (positions['concentration'][0], index-1)

        return positions

    @staticmethod
    def increase_value_index(value_index, values, symbol, label, element_data):
        value_index += 1

        if value_index < len(values) and values[value_index] == '?':
            message = "Suspect value for element %s, %s = %0.4f" % (symbol, label, element_data[symbol][label])
            warnings.warn(message)

            value_index += 1

        return value_index

    def read_intensity_lines(self, lines, element_data):
        for line in lines:
            line = line.strip()

            if len(line) > 0:
                values = line.split()

                symbol = values[1]

                element_data.setdefault(symbol, {})

                element_data[symbol]['id'] = int(values[0])

                value_index = 2

                label = 'peak_mm'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'net_cps'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'bg-_cps'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'bg+_cps'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'sd_%%'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'dl_ppm'
                element_data[symbol][label] = float(values[value_index])

                self.increase_value_index(value_index, values, symbol, label, element_data)

    def read_correction_lines(self, lines, element_data):
        for line in lines:
            line = line.strip()

            if len(line) > 0:
                values = line.split()

                symbol = values[0]

                element_data.setdefault(symbol, {})

                value_index = 1

                label = 'f(chi)'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'If/Ip'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'abs-el'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = '1/s-el'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'r-el'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'c/k-el'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'c/k-std'
                element_data[symbol][label] = float(values[value_index])

                self.increase_value_index(value_index, values, symbol, label, element_data)

    def read_concentration_lines(self, lines, element_data):
        for line in lines:
            line = line.strip()

            if len(line) > 0:
                values = line.split()

                symbol = values[0]

                element_data.setdefault(symbol, {})

                value_index = 1

                label = 'El fw'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'Ox fw'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'Norm El'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'Norm Ox'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'Atomic'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'k-value'
                element_data[symbol][label] = float(values[value_index])

                value_index = self.increase_value_index(value_index, values, symbol, label, element_data)

                label = 'k-std'
                element_data[symbol][label] = float(values[value_index])

                self.increase_value_index(value_index, values, symbol, label, element_data)

    @staticmethod
    def read_total_lines(lines, element_data):
        values = lines[0][7:].split()

        element_data['total'] = {}

        element_data['total']['El fw'] = float(values[0])

        element_data['total']['Ox fw'] = float(values[1])

        element_data['total']['Norm El'] = float(values[2])

        element_data['total']['Norm Ox'] = float(values[3])

        element_data['total']['Atomic'] = float(values[4])

    def read_lines(self, lines):
        line_index = 0
        self.spectrum_id = self.read_id_line(lines[line_index])

        line_index += 1
        self.group, self.sample = self.read_group_sample_line(lines[line_index])

        line_index += 1
        self.number, self.comment = self.read_number_comment_line(lines[line_index])

        line_index += 1
        self.stage_x, self.stage_y, self.stage_z = self.read_stage_line(lines[line_index])

        line_index += 1
        self.incident_energy_keV, self.probe_diameter, self.scan_on = self.read_beam_line(lines[line_index])

        line_index += 1
        self.date = self.read_date_line(lines[line_index])

        line_index += 1
        self.detector_type, self.number_accumulation = self.read_detector_line(lines[line_index])

        line_index += 1

        line_index += 1
        self.current_A = self.read_current_line(lines[line_index])

        line_index += 1
        positions = self.get_positions(lines)

        self.element_data = {}

        start, end = positions['intensity']
        self.read_intensity_lines(lines[start:end], self.element_data)

        start, end = positions['correction']
        self.read_correction_lines(lines[start:end], self.element_data)

        start, end = positions['concentration']
        self.read_concentration_lines(lines[start:end], self.element_data)

        start, end = positions['total']
        self.read_total_lines(lines[start:end], self.element_data)

        return self.spectrum_id

    def get_value(self, label, symbol=None):
        if symbol is None:
            if label == 'id':
                return self.spectrum_id

            if label == 'group':
                return self.group

            if label == 'sample':
                return self.sample

            if label == 'number':
                return self.number

            if label == 'comment':
                return self.comment

            if label == 'stage_x':
                return self.stage_x

            if label == 'stage_y':
                return self.stage_y

            if label == 'stage_z':
                return self.stage_z

            if label == 'incident_energy_keV':
                return self.incident_energy_keV

            if label == 'probe_diameter':
                return self.probe_diameter

            if label == 'scan_on':
                return self.scan_on

            if label == 'date':
                return self.date

            if label == 'detector_type':
                return self.detector_type

            if label == 'number_accumulation':
                return self.number_accumulation

            if label == 'current_A':
                return self.current_A

        elif symbol in self.element_data:
            if symbol == 'total':
                if label in self.element_data['total']:
                    return self.element_data['total'][label]
            else:
                if label in self.element_data[symbol]:
                    return self.element_data[symbol][label]

        return 0.0


class JEOL8900McGill:
    def __init__(self, filename):
        self.points = None
        self.master_header = None

        self.read_results_file(filename)

    def read_results_file(self, filename):
        lines = open(filename, 'r').readlines()

        points_index = []

        for line in lines:

            if 'Intensity' in line:
                self.read_master_header(line)

            if 'Unknown Specimen No.' in line:
                points_index.append(lines.index(line))

            if len(line) == 0:
                pass

        self.points = {}

        for index in points_index:
            self.read_point_data(lines[index:index + 30])

        return len(lines)

    def read_point_data(self, lines):
        point = DataPoint()

        spectrum_id = point.read_lines(lines)

        self.points[spectrum_id] = point

    def read_master_header(self, line):
        keywords = ['Intensity', 'Group', 'Sample', 'Page']

        position_keywords = []

        for keyword in keywords:
            position = line.find(keyword)

            position_keywords.append(position)

        self.master_header = {}

    def get_values_list(self, label, symbol=None):
        ids = self.points.keys()
        ids.sort()

        values = []

        for spectrumID in ids:
            if symbol is None:
                value = self.points[spectrumID].get_value(label)

                values.append(value)
            elif symbol is not None:
                value = self.points[spectrumID].get_value(label, symbol)

                values.append(value)

        return ids, values
