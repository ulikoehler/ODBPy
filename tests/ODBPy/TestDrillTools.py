#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.DrillTools import *
from ODBPy.Structures import *
from ODBPy.StructuredTextParser import *
from .TestStructuredTextParser import testDrillTools
from io import StringIO

class TestDrillTools (object):
    def test_parser(self):
        expected = DrillToolSet({"THICKNESS": 0, "USER_PARAMS": ""}, {
            1: DrillTool(1, HolePlating.Via, DrillToolType.Standard, 12, {
                "MIN_TOL": 0,
                "MAX_TOL": 0,
                "BIT": "",
                "FINISH_SIZE": 12
            }),
            2: DrillTool(2, HolePlating.NonPlated, DrillToolType.Standard, 39.3701, {
                "MIN_TOL": 0,
                "MAX_TOL": 0,
                "BIT": "",
                "FINISH_SIZE": 39.3701,
            })
        })
        actual = parse_drill_tools(parse_structured_text(StringIO(testDrillTools)))
        assert_equal(expected, actual)


