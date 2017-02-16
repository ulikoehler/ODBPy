#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from io import StringIO
from ODBPy.Profile import *
from ODBPy.LineRecordParser import *
from ODBPy.Structures import *
from ODBPy.SurfaceParser import *
from ODBPy.PolygonParser import *
from ODBPy.Decoder import *

testProfile = """
#
#Units
#
U MM

#
#Layer features
#
S P 0
OB -38.104 -0.6351 I
OS -38.104 19.3649
OS -18.104 19.3649
OS -18.104 -0.6351
OS -38.104 -0.6351
OE
SE
"""

class TestProfile(object):

    def test_parse_profile(self):
        expected = Profile("MM", [Surface(Polarity.Positive, 0, [
            Polygon(PolygonType.Island, [
                PolygonSegment(start=Point(x=-38.104, y=-0.6351), end=Point(x=-38.104, y=19.3649)),
                PolygonSegment(start=Point(x=-38.104, y=19.3649), end=Point(x=-18.104, y=19.3649)),
                PolygonSegment(start=Point(x=-18.104, y=19.3649), end=Point(x=-18.104, y=-0.6351)),
                PolygonSegment(start=Point(x=-18.104, y=-0.6351), end=Point(x=-38.104, y=-0.6351))
            ])
        ], {})])
        actual = parse_profile(read_linerecords(StringIO(testProfile)))
        print(actual)
        assert_equal(expected, actual)
