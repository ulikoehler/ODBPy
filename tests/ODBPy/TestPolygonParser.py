#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.PolygonParser import *
from ODBPy.Structures import *
from ODBPy.Decoder import *

class TestPolygonParser(object):

    def test_parse_ob(self):
        assert_equal(PolygonBeginTag(Point(0, 0), PolygonType.Island),
            run_decoder_on_line("OB 0 0 I", polygon_decoder_options))
        assert_equal(PolygonBeginTag(Point(3.1, 2.4), PolygonType.Hole),
            run_decoder_on_line("OB 3.1 2.4 H", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OB H", polygon_decoder_options))

    def test_parse_os(self):
        assert_equal(PolygonSegmentTag(Point(0, 0)),
            run_decoder_on_line("OS 0 0", polygon_decoder_options))
        assert_equal(PolygonSegmentTag(Point(0, 50)),
            run_decoder_on_line("OS 0 50", polygon_decoder_options))
        assert_equal(PolygonSegmentTag(Point(22.5, 15)),
            run_decoder_on_line("OS 22.5 15", polygon_decoder_options))

        assert_is_none(run_decoder_on_line("OS 22.5", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OS", polygon_decoder_options))

    def test_parse_os(self):
        assert_equal(PolygonCircleTag(Point(0, 0), Point(1, 1), CircleDirection.Clockwise),
            run_decoder_on_line("OC 0 0 1 1 Y", polygon_decoder_options))
        assert_equal(PolygonCircleTag(Point(0, 1), Point(2, 3), CircleDirection.Clockwise),
            run_decoder_on_line("OC 0 1 2 3 Y", polygon_decoder_options))
        assert_equal(PolygonCircleTag(Point(0.1, 1.2), Point(2.3, 3.4), CircleDirection.Clockwise),
            run_decoder_on_line("OC 0.1 1.2 2.3 3.4 Y", polygon_decoder_options))
        assert_equal(PolygonCircleTag(Point(0.1, 1.2), Point(2.3, 3.4), CircleDirection.CounterClockwise),
            run_decoder_on_line("OC 0.1 1.2 2.3 3.4 N", polygon_decoder_options))

        assert_is_none(run_decoder_on_line("OC", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OC 0", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OC 0 0", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OC 0 0 0", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OC 0 0 0 0", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OC 0 0 0 0 X", polygon_decoder_options))

    def test_parse_oe(self):
        assert_equal(PolygonEndTag(), run_decoder_on_line("OE", polygon_decoder_options))
        assert_is_none(run_decoder_on_line("OE 1", polygon_decoder_options))

