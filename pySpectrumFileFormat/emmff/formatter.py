#!/usr/bin/env python
"""
================================================================================
:mod:`formatter` -- Parse values from XML string
================================================================================

.. module:: formatter
   :synopsis: Parse values from XML string

"""

# Script information for the file.
__author__ = "Philippe T. Pinard"
__email__ = "philippe.pinard@gmail.com"
__version__ = "0.1"
__copyright__ = "Copyright (c) 2010 Philippe T. Pinard"
__license__ = "GPL v3"

# Standard library modules.
import types
import numbers

# Third party modules.

# Local modules.

# Globals and constants variables.

class NoMatch(Exception):
    pass

class _Condition:
    def __str__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return self.__class__.__name__ == other.__class__.__name__

    def __ne__(self, other):
        return not self == other

    def from_string(self, value):
        raise NoMatch

    def to_string(self, value):
        raise NoMatch

class TrueFalseCondition(_Condition):
    def from_string(self, value):
        trues = ['true', 'yes']
        falses = ['false', 'no']

        tmpvalue = value.strip().lower()

        if tmpvalue in trues:
            return True
        elif tmpvalue in falses:
            return False
        else:
            raise NoMatch

    def to_string(self, value):
        if isinstance(value, bool):
            if value:
                return "true"
            else:
                return "false"
        else:
            raise NoMatch

class NoneCondition(_Condition):
    def from_string(self, value):
        if value.strip().lower() == 'none':
            return None
        else:
            raise NoMatch

    def to_string(self, value):
        if isinstance(value, type(None)):
            return "none"
        else:
            raise NoMatch

class NumberCondition(_Condition):
    def from_string(self, value):
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                try:
                    value = complex(value)
                except ValueError:
                    raise NoMatch

        return value

    def to_string(self, value):
        if isinstance(value, numbers.Number) and not isinstance(value, bool):
            return str(value)
        else:
            raise NoMatch

class Formatter:
    def __init__(self):
        self._conditions = []

    def register(self, condition):
        if not condition in self._conditions:
            self._conditions.append(condition)

    def deregister(self, condition):
        if condition in self._conditions:
            self._conditions.pop(condition)
        else:
            raise ValueError("Condition (%s) is not registered.")

    def _run(self, value, meth):
        matches = []

        # Loop through the condition
        for condition in self._conditions:
            try:
                result = getattr(condition, meth)(value)
            except NoMatch:
                continue

            matches.append((str(condition), result))

        if not matches:
            return value
        elif len(matches) > 1:
            error = "Found multiple formatting matches for value (%s)\n" % value
            for condition, result in matches:
                error += "- %s (%s)\n" % (result, condition)
            raise ValueError(error)
        else:
            return matches[0][1]

    def from_string(self, value):
        return self._run(value, "from_string")

    def to_string(self, value):
        return self._run(value, "to_string")

formatter = Formatter()
formatter.register(TrueFalseCondition())
formatter.register(NoneCondition())
formatter.register(NumberCondition())
