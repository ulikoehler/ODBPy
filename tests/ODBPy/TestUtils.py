#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, raises, assert_is_none
from ODBPy.Utils import *

class TestUtils(object):
    def test_try_parse_number(self):
        assert_equal("01", try_parse_number("01"))
        assert_equal(0, try_parse_number("0"))
        assert_equal(0.1, try_parse_number("0.1"))

