#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.LineRecordParser import *
from io import StringIO

testLineRecords = """
#
#Units
#
U MM

#
#Layer features
#
S P 0"""

class TestLineRecordParser(object):
    def test_parser(self):
        assert_equal({"Units":["U MM"], "Layer features": ["S P 0"]},
            read_linerecords(StringIO(testLineRecords)))
        

