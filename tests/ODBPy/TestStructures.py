#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_almost_equal, assert_false, raises, assert_is_none
from ODBPy.Structures import *

class TestPoint(object):
    def test_add(self):
        assert_equal(Point(4, 10), Point(1, 1) + Point(3, 9))
        assert_equal(Point(4, 12), Point(1, 9) + 3)

    def test_sub(self):
        assert_equal(Point(-2, -8), Point(1, 1) - Point(3, 9))
        assert_equal(Point(-2, 6), Point(1, 9) - 3)

    def test_mul(self):
        assert_equal(Point(3, 8), Point(1, 2) * Point(3, 4))
        assert_equal(Point(-3, -27), Point(1, 9) * -3)

    def test_div(self):
        assert_equal(Point(1, 2), Point(3, 8) / Point(3, 4))
        assert_equal(Point(1, 9), Point(-3, -27) / -3)
