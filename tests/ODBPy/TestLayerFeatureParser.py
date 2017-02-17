#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.LayerFeatureParser import *
from ODBPy.Structures import *
from ODBPy.Decoder import *

class TestPadParsing(object):
    def _parse_pad(self, s):
        pads = list(decode_features({
            "Layer features": [s]
        }))
        assert_equal(len(pads), 1)
        return pads[0]

    def test_parse_pad_realdata(self):
        """Test pad parsing with DipTrace-generated data"""
        expected = Pad(Point(-30.9595, 3.8107),
            SymbolReference(0, 1.0), Polarity.Positive, 0, Mirror.No, 0., {0:0, 2:0})
        assert_equal(expected, self._parse_pad("P -30.9595 3.8107 0 P 0 8 0;0=0,2=0"))

    def test_parse_pad_stddoc(self):
        """Test parsing pads from the ODB++ specification, v7.0 p. 113"""
        assert_equal(Pad(Point(1., 2.), SymbolReference(0, 1.0),
            Polarity.Positive, 4, Mirror.No, 90, {}),
            self._parse_pad("P 1.0 2.0 0 P 4 1"))
        assert_equal(Pad(Point(1., 2.), SymbolReference(0, 1.0),
            Polarity.Positive, 4, Mirror.No, 30, {}),
            self._parse_pad("P 1.0 2.0 0 P 4 8 30.0"))
        assert_equal(Pad(Point(1., 2.), SymbolReference(0, 0.02),
            Polarity.Positive, 4, Mirror.No, 90, {}),
            self._parse_pad("P 1.0 2.0 -1 0 0.02 P 4 1"))
        assert_equal(Pad(Point(1., 2.), SymbolReference(0, 0.02),
            Polarity.Positive, 4, Mirror.No, 30, {}),
            self._parse_pad("P 1.0 2.0 -1 0 0.02 P 4 8 30.0"))


class TestLineParsing(object):
    def _parse_line(self, s):
        lines = list(decode_features({
            "Layer features": [s]
        }))
        assert_equal(len(lines), 1)
        return lines[0]

    def test_parse_line_realdata(self):
        """Test line parsing with DipTrace-generated data"""
        expected = Line(Point(4.8298, -44.2445), Point(4.8298, -45.2654),
            SymbolReference(14, 1.0), Polarity.Positive, 0, {})
        assert_equal(expected, self._parse_line("L 4.8298 -44.2445 4.8298 -45.2654 14 P 0"))
        # With attributes
        expected = Line(Point(4.8298, -44.2445), Point(4.8298, -45.2654),
            SymbolReference(14, 1.0), Polarity.Positive, 0, {0:0, 2:0})
        assert_equal(expected, self._parse_line("L 4.8298 -44.2445 4.8298 -45.2654 14 P 0;0=0,2=0"))

