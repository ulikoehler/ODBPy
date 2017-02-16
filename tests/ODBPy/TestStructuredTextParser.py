#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.StructuredTextParser import *
from io import StringIO

testStructuredText = """
THICKNESS=0
USER_PARAMS=

TOOLS {
    NUM=1
    TYPE=VIA
    TYPE2=STANDARD
    MIN_TOL=0
    MAX_TOL=0
    BIT=
    FINISH_SIZE=12
    DRILL_SIZE=12
}
(
TOOLS {
    NUM=2
    TYPE=NON_PLATED
    TYPE2=STANDARD
    MIN_TOL=0
    MAX_TOL=0
    BIT=
    FINISH_SIZE=39.3701
    DRILL_SIZE=39.3701
}"""

class TestStructuredTextParser(object):
    def test_parser(self):
        expected = StructuredText({"THICKNESS": 0, "USER_PARAMS": ""}, [
            StructuredArray("TOOLS", {
                "NUM": 1,
                "TYPE": "VIA",
                "TYPE2": "STANDARD",
                "MIN_TOL": 0,
                "MAX_TOL": 0,
                "BIT": "",
                "FINISH_SIZE": 12,
                "DRILL_SIZE": 12
            }), StructuredArray("TOOLS", {
                "NUM": 2,
                "TYPE": "NON_PLATED",
                "TYPE2": "STANDARD",
                "MIN_TOL": 0,
                "MAX_TOL": 0,
                "BIT": "",
                "FINISH_SIZE": 39.3701,
                "DRILL_SIZE": 39.3701
            })
        ])
        actual = parse_structured_text(StringIO(testStructuredText))
        assert_equal(expected, actual)


