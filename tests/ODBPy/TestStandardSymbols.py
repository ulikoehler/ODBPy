#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, raises, assert_is_none
from ODBPy.StandardSymbols import *

class TestStandardSymbolParsing(object):
    def testRound(self):
        assert_equal(Round(40.), Round.Parse("r40"))
        assert_equal(Round(3.5), Round.Parse("r3.5"))
        assert_is_none(Round.Parse("rabc"))
        assert_is_none(Round.Parse("s3.5"))

    def testSquare(self):
        assert_equal(Square(40.), Square.Parse("s40"))
        assert_equal(Square(3.5), Square.Parse("s3.5"))
        assert_is_none(Square.Parse("rabc"))
        assert_is_none(Square.Parse("r3.5"))

    def testRectangle(self):
        assert_equal(Rectangle(60., 30.), Rectangle.Parse("r60x30"))
        assert_equal(Rectangle(1., 2), Rectangle.Parse("r1x2"))
        assert_equal(Rectangle(5.1, 3.33), Rectangle.Parse("r5.1x3.33"))
        assert_is_none(Rectangle.Parse("rabc"))
        assert_is_none(Rectangle.Parse("r3.5"))

