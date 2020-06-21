#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. py:currentmodule:: microanalysis_file_format.emmff.emsa_format

.. moduleauthor:: Hendrix Demers <hendrix.demers@mail.mcgill.ca>

Reader/writer of EMSA/MAS file format.
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
import logging

# Third party modules.

# Local modules.

# Project modules.

# Globals and constants variables.


class RequiredKeyword:
    format = "FORMAT"
    version = "VERSION"
    title = "TITLE"
    date = "DATE"
    time = "TIME"
    owner = "OWNER"
    number_points = "NPOINTS"
    number_columns = "NCOLUMNS"
    x_units = "XUNITS"
    y_units = "YUNITS"
    data_type = "DATATYPE"
    x_per_channel = "XPERCHAN"
    offset = "OFFSET"


class SpectrumDataKeyword:
    spectrum = "SPECTRUM"
    end_of_data = "ENDOFDATA"


class OptionalKeyword:
    # Keywords relating mainly to spectrum characteristics.
    signal_type = "SIGNALTYPE"
    x_units = "XUNITS"
    y_units = "YUNITS"
    x_label = "XLABEL"
    y_label = "YLABEL"
    channel_offset = "CHOFFSET"
    comment = "COMMENT"
    # Keywords relating mainly to microscope/instrument.
    beam_energy = "BEAMKV"
    emission_current = "EMISSION"
    probe_current = "PROBECUR"
    beam_diameter = "BEAMDIAM"
    magnification = "MAGCAM"
    convergence_angle = "CONVANGLE"
    operating_mode = "OPERMODE"
    # Keywords relating mainly to specimen.
    thickness = "THICKNESS"
    x_stage_tilt = "XTILISTGE"
    y_stage_tilt = "YTILISTGE"
    x_position = "XPOSITION"
    y_position = "YPOSITION"
    z_position = "ZPOSITION"
    # Keywords relating mainly to ELS.
    dwell_time = "DWELLTIME"
    integration_time = "INTEGTIME"
    collection_angle = "COLLANGLE"
    els_detector_type = "ELSDET"
    # Keywords relating mainly to EDS.
    elevation_angle = "ELEVANGLE"
    azimuthal_angle = "AZIMANGLE"
    solid_angle = "SOLIDANGLE"
    live_time = "LIVETIME"
    real_time = "REALTIME"
    be_window_thickness = "TBEWIND"
    au_contact_thickness = "TAUWIND"
    dead_layer_thickness = "TDEADLYR"
    active_layer_thickness = "TACTLYR"
    aluminium_window_thickness = "TALWIND"
    pyrolene_window_thickness = "TPYWIND"
    boron_nitride_window_thickness = "TBNWIND"
    diamond_window_thickness = "TDIWIND"
    hydro_carbon_window_thickness = "THCWIND"
    eds_detector_type = "EDSDET"
    checksum = "CHECKSUM"


class OptionalUserDefinedKeyword:
    class OxfordInstruments:
        element = "OXINSTELEMS"
        label = "OXINSTLABEL"


class EmsaFormat:
    def __init__(self, filename=None, lines=None):
        self.lines = lines
        self.filename = filename
        self.values = []
        self.x_data = []
        self.y_data = []

        self.keywords = []

        self.header = {}

        self.is_file_valid = None

        self.set_function = {}
        self.set_function[RequiredKeyword.format] = 'set_format'
        self.set_function[RequiredKeyword.version] = 'set_version'
        self.set_function[RequiredKeyword.title] = 'set_title'
        self.set_function[RequiredKeyword.date] = 'set_date'
        self.set_function[RequiredKeyword.time] = 'set_time'
        self.set_function[RequiredKeyword.owner] = 'set_owner'
        self.set_function[RequiredKeyword.number_points] = 'set_number_points'
        self.set_function[RequiredKeyword.number_columns] = 'set_number_columns'
        self.set_function[RequiredKeyword.x_units] = 'set_x_units'
        self.set_function[RequiredKeyword.y_units] = 'set_y_units'
        self.set_function[RequiredKeyword.data_type] = 'set_data_type'
        self.set_function[RequiredKeyword.x_per_channel] = 'set_x_per_channel'
        self.set_function[RequiredKeyword.offset] = 'set_offset'

        self.set_function[OptionalKeyword.signal_type] = 'set_signal_type'
        self.set_function[OptionalKeyword.channel_offset] = 'set_channel_offset'
        self.set_function[OptionalKeyword.live_time] = 'set_live_time'
        self.set_function[OptionalKeyword.real_time] = 'set_real_time'
        self.set_function[OptionalKeyword.beam_energy] = 'set_beam_energy'
        self.set_function[OptionalKeyword.probe_current] = 'set_probe_current'
        self.set_function[OptionalKeyword.magnification] = 'set_magnification'
        self.set_function[OptionalKeyword.x_position] = 'set_x_position'
        self.set_function[OptionalKeyword.y_position] = 'set_y_position'
        self.set_function[OptionalKeyword.z_position] = 'set_z_position'

        self.set_function[OptionalUserDefinedKeyword.OxfordInstruments.element] = 'set_oxford_instruments_element'
        self.set_function[OptionalUserDefinedKeyword.OxfordInstruments.label] = 'set_oxford_instruments_label'

        if self.filename is not None:
            self.open(self.filename)
            self.read_lines()
            self.set_header()
            self.set_spectrum_data()

    def open(self, filename):
        try:
            self.lines = open(filename).readlines()
        except OSError and TypeError:
            raise IOError

    def is_line_data(self, line):
        """Check if the line is a valid data. Return True or False, type (Y, XY),
        and number of column (1--5)."""

        if line is None or line.strip().startswith('#'):
            return False, None, 0

        data_type = self.get_data_type()

        if data_type == 'Y':
            # Y with 1 column
            try:
                _ = float(line)

                return True, 'Y', 1
            except ValueError:
                pass

            # Y with comma 2 to 5 column
            try:
                y_value_list = line.split(',')

                if 1 < len(y_value_list) <= 5:
                    new_y_values = []
                    for y_value in y_value_list:
                        try:
                            y_value = float(y_value)
                            new_y_values.append(y_value)
                        except ValueError:
                            pass

                    return True, 'Y', len(new_y_values)
            except ValueError:
                pass

            # Y with space 2 to 5 column
            try:
                y_value_list = line.split()

                if 1 < len(y_value_list) <= 5:
                    for y_value in y_value_list:
                        _ = float(y_value)

                    return True, 'Y', len(y_value_list)
            except ValueError:
                pass
        elif data_type == 'XY':
            # XY with comma
            try:
                x_value, y_value = line.split(',')

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass

            # XY with comma
            try:
                x_value, y_value, dummy = line.split(',')

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass

            # XY with space
            try:
                x_value, y_value = line.split()

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass
        else:
            # Y with 1 column
            try:
                _ = float(line)

                return True, 'Y', 1
            except ValueError:
                pass

            # Y with comma 2 to 5 column
            try:
                y_value_list = line.split(',')

                if 1 < len(y_value_list) <= 5:
                    number_values = 0
                    for y_value in y_value_list:
                        try:
                            _ = float(y_value)
                            number_values += 1
                        except ValueError:
                            pass

                    return True, 'Y', number_values
            except ValueError:
                pass

            # Y with space 2 to 5 column
            try:
                y_value_list = line.split()

                if 1 < len(y_value_list) <= 5:
                    for y_value in y_value_list:
                        _ = float(y_value)

                    return True, 'Y', len(y_value_list)
            except ValueError:
                pass

            # XY with comma
            try:
                x_value, y_value = line.split(',')

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass

            # XY with comma
            try:
                x_value, y_value, dummy = line.split(',')

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass

            # XY with space
            try:
                x_value, y_value = line.split()

                _ = float(x_value)
                _ = float(y_value)

                return True, 'XY', 2
            except ValueError:
                pass

        return False, None, 0

    @staticmethod
    def is_line_keyword(line):
        try:
            if line.strip()[0] == '#':
                return True
        except (ValueError, IndexError, AttributeError):
            pass

        return False

    @staticmethod
    def read_keyword_line(line):
        start_keyword_position = 1
        end_keyword_position = 13
        start_data_position = 15

        keyword = None
        keyword_comment = None
        data = None

        try:
            if line[0] == '#':
                if line[1] == '#':
                    keyword = line[start_keyword_position+1:end_keyword_position]
                    data = line[start_data_position:]
                else:
                    keyword = line[start_keyword_position:end_keyword_position]
                    data = line[start_data_position:]

                keyword = keyword.strip()
                keyword_comment = ""

                try:
                    new_keyword, keyword_comment = keyword.split()
                    keyword = new_keyword
                except ValueError:
                    pass

                keyword = keyword.strip()
                keyword = keyword.upper()

                keyword_comment = keyword_comment.strip()

                data = data.strip()

        except IndexError:
            pass

        return keyword, keyword_comment, data

    @staticmethod
    def read_data_line(line):
        try:
            values = line.split()
            for index, item in enumerate(values):
                values[index] = float(item)
            return values
        except ValueError:
            pass

        try:
            values = []
            for index, item in enumerate(line.split(',')):
                try:
                    values.append(float(item))
                except ValueError:
                    pass
            if len(values) > 0:
                return values
            else:
                return None
        except ValueError:
            pass

        return None

    def read_line(self, line):
        if self.is_line_keyword(line):
            keyword, keyword_comment, data = self.read_keyword_line(line)
            if keyword:
                keyword_data = {}
                keyword_data["keyword"] = keyword
                keyword_data["comment"] = keyword_comment
                keyword_data["data"] = data
                keyword_data["order"] = len(self.keywords)+1

                self.keywords.append(keyword_data)

        if self.is_line_data(line)[0]:
            values = self.read_data_line(line)
            if values:
                self.values.append(values)

    def read_lines(self):
        if self.lines:
            for line in self.lines:
                self.read_line(line)

    def set_header(self):
        check_order = 0
        self.is_file_valid = True

        for keyword in self.keywords:
            check_order += 1
            for variable in RequiredKeyword.__dict__.keys():
                if RequiredKeyword.__dict__.get(variable, None) == keyword["keyword"]:
                    if RequiredKeyword.__dict__[variable] in self.set_function:
                        function = EmsaFormat.__dict__[self.set_function[RequiredKeyword.__dict__[variable]]]
                        function(self, keyword["data"])
                        if check_order != keyword["order"]:
                            print("Warning keyword in the wrong order.")
                            self.is_file_valid = False

            for variable in OptionalKeyword.__dict__.keys():
                if OptionalKeyword.__dict__.get(variable, None) == keyword["keyword"]:
                    if OptionalKeyword.__dict__[variable] in self.set_function:
                        function = EmsaFormat.__dict__[self.set_function[OptionalKeyword.__dict__[variable]]]
                        function(self, keyword["data"])
                        if check_order != keyword["order"]:
                            print("Warning keyword in the wrong order.")
                            self.is_file_valid = False

            for variable in OptionalUserDefinedKeyword.OxfordInstruments.__dict__.keys():
                if OptionalUserDefinedKeyword.OxfordInstruments.__dict__.get(variable, None) == keyword["keyword"]:
                    if OptionalUserDefinedKeyword.OxfordInstruments.__dict__[variable] in self.set_function:
                        function = EmsaFormat.__dict__[self.set_function[
                            OptionalUserDefinedKeyword.OxfordInstruments.__dict__[variable]]]
                        function(self, keyword["data"])
                        if check_order != keyword["order"]:
                            print("Warning keyword in the wrong order.")
                            self.is_file_valid = False

    def set_format(self, new_format):
        self.header[RequiredKeyword.format] = new_format

    def get_format(self):
        return self.header.get(RequiredKeyword.format, None)

    def set_version(self, new_version):
        self.header[RequiredKeyword.version] = new_version

    def get_version(self):
        return self.header.get(RequiredKeyword.version, None)

    def set_title(self, new_value):
        self.header[RequiredKeyword.title] = new_value

    def get_title(self):
        return self.header.get(RequiredKeyword.title, None)

    def set_date(self, new_value):
        self.header[RequiredKeyword.date] = new_value

    def get_date(self):
        return self.header.get(RequiredKeyword.date, None)

    def set_time(self, new_value):
        self.header[RequiredKeyword.time] = new_value

    def get_time(self):
        return self.header.get(RequiredKeyword.time, None)

    def set_owner(self, new_value):
        self.header[RequiredKeyword.owner] = new_value

    def get_owner(self):
        return self.header.get(RequiredKeyword.owner, None)

    def set_number_points(self, new_value):
        self.header[RequiredKeyword.number_points] = float(new_value)

    def get_number_points(self):
        return self.header.get(RequiredKeyword.number_points, None)

    def set_number_columns(self, new_value):
        self.header[RequiredKeyword.number_columns] = float(new_value)

    def get_number_columns(self):
        return self.header.get(RequiredKeyword.number_columns, None)

    def set_x_units(self, new_value):
        self.header[RequiredKeyword.x_units] = new_value

    def get_x_units(self):
        return self.header.get(RequiredKeyword.x_units, None)

    def set_y_units(self, new_value):
        self.header[RequiredKeyword.y_units] = new_value

    def get_y_units(self):
        return self.header.get(RequiredKeyword.y_units, None)

    def set_data_type(self, new_value):
        self.header[RequiredKeyword.data_type] = new_value

    def get_data_type(self):
        return self.header.get(RequiredKeyword.data_type, None)

    def set_x_per_channel(self, new_value):
        self.header[RequiredKeyword.x_per_channel] = float(new_value)

    def get_x_per_channel(self):
        return self.header.get(RequiredKeyword.x_per_channel, None)

    def set_offset(self, new_value):
        self.header[RequiredKeyword.offset] = float(new_value)

    def get_offset(self):
        return self.header.get(RequiredKeyword.offset, None)

    def set_signal_type(self, new_value):
        self.header[OptionalKeyword.signal_type] = new_value

    def get_signal_type(self):
        return self.header.get(OptionalKeyword.signal_type, None)

    def set_channel_offset(self, new_value):
        self.header[OptionalKeyword.channel_offset] = float(new_value)

    def get_channel_offset(self):
        return self.header.get(OptionalKeyword.channel_offset, None)

    def set_live_time(self, new_value):
        self.header[OptionalKeyword.live_time] = float(new_value)

    def get_live_time(self):
        return self.header.get(OptionalKeyword.live_time, None)

    def set_real_time(self, new_value):
        self.header[OptionalKeyword.real_time] = float(new_value)

    def get_real_time(self):
        return self.header.get(OptionalKeyword.real_time, None)

    def set_beam_energy(self, new_value):
        self.header[OptionalKeyword.beam_energy] = float(new_value)

    def get_beam_energy(self):
        return self.header.get(OptionalKeyword.beam_energy, None)

    def set_probe_current(self, new_value):
        self.header[OptionalKeyword.probe_current] = float(new_value)

    def get_probe_current(self):
        return self.header.get(OptionalKeyword.probe_current, None)

    def set_magnification(self, new_value):
        self.header[OptionalKeyword.magnification] = float(new_value)

    def get_magnification(self):
        return self.header.get(OptionalKeyword.magnification, None)

    def set_x_position(self, new_value):
        self.header[OptionalKeyword.x_position] = float(new_value)

    def get_x_position(self):
        return self.header.get(OptionalKeyword.x_position, None)

    def set_y_position(self, new_value):
        self.header[OptionalKeyword.y_position] = float(new_value)

    def get_y_position(self):
        return self.header.get(OptionalKeyword.y_position, None)

    def set_z_position(self, new_value):
        self.header[OptionalKeyword.z_position] = float(new_value)

    def get_z_position(self):
        return self.header.get(OptionalKeyword.z_position, None)

    def set_oxford_instruments_element(self, new_value):
        self.header[OptionalUserDefinedKeyword.OxfordInstruments.element] = new_value

    def get_oxford_instruments_element(self):
        return self.header.get(OptionalUserDefinedKeyword.OxfordInstruments.element, None)

    def set_oxford_instruments_label(self, new_value):
        self.header[OptionalUserDefinedKeyword.OxfordInstruments.label] = new_value

    def get_oxford_instruments_label(self):
        return self.header.get(OptionalUserDefinedKeyword.OxfordInstruments.label, None)

    def set_spectrum_data(self):
        data_type = self.get_data_type()
        number_columns = self.get_number_columns()

        if data_type and number_columns:
            for values in self.values:
                if data_type == "XY":
                    try:
                        self.x_data.append(values[0])
                        self.y_data.append(values[1])
                    except IndexError as message:
                        logging.error(message)
                        logging.info(values)
                        logging.info(self.filename)
                elif data_type == "Y":
                    for item in values:
                        if isinstance(item, list):
                            self.y_data.extend(item)
                        else:
                            self.y_data.append(item)
            if data_type == "Y":
                number_points = self.get_number_points()
                if len(self.y_data) != number_points:
                    number_points = len(self.y_data)

                self.x_data = self.create_x_data(number_points, self.get_offset(), self.get_x_per_channel())

    def get_data_x(self):
        return self.x_data

    def get_data_y(self):
        return self.y_data

    def get_data(self):
        data = []
        assert(len(self.x_data) == len(self.y_data))
        for index in range(len(self.x_data)):
            data.append((self.x_data[index], self.y_data[index]))

        return data

    @staticmethod
    def create_x_data(number_points, offset, x_per_channel):
        x_data = []
        for index in range(int(number_points)):
            x_data.append(offset + x_per_channel * index)

        return x_data
