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
