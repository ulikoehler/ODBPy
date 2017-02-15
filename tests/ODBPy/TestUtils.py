#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.Utils import *

class TestUtils(object):
    def test_try_parse_number(self):
        assert_equal("01", try_parse_number("01"))
        assert_equal(0, try_parse_number("0"))
        assert_equal(0.1, try_parse_number("0.1"))

    def test_const_false(self):
        assert_false(const_false())

    def test_not_none(self):
        assert_false(not_none(None))
        assert_true(not_none(1))
        assert_true(not_none(0))
        assert_true(not_none(""))

