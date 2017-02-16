#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.Attributes import *

class TestAttributes(object):
    def test_parse_attributes_from_line(self):
        assert_equal({0: 0, 2: 0}, parse_attributes_from_line(
            "P -30.9595 3.8107 0 P 0 8 0;0=0,2=0"))
        assert_equal({}, parse_attributes_from_line(
            "P -30.9595 3.8107 0 P 0 8 0"))
