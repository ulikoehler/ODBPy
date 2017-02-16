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
        assert_is_none(Square.Parse("sabc"))
        assert_is_none(Square.Parse("r3.5"))

    def testRectangle(self):
        assert_equal(Rectangle(60., 30.), Rectangle.Parse("r60x30"))
        assert_equal(Rectangle(1., 2), Rectangle.Parse("r1x2"))
        assert_equal(Rectangle(5.1, 3.33), Rectangle.Parse("r5.1x3.33"))
        assert_is_none(Rectangle.Parse("rabc"))
        assert_is_none(Rectangle.Parse("r3.5"))
        assert_is_none(Rectangle.Parse("r1x2x3"))

    def testOval(self):
        assert_equal(Oval(60., 30.), Oval.Parse("oval60x30"))
        assert_equal(Oval(1., 2), Oval.Parse("oval1x2"))
        assert_equal(Oval(5.1, 3.33), Oval.Parse("oval5.1x3.33"))
        assert_is_none(Oval.Parse("ovalabc"))
        assert_is_none(Oval.Parse("oval3.5"))

    def testDiamond(self):
        assert_equal(Diamond(60., 30.), Diamond.Parse("di60x30"))
        assert_equal(Diamond(1., 2), Diamond.Parse("di1x2"))
        assert_equal(Diamond(5.1, 3.33), Diamond.Parse("di5.1x3.33"))
        assert_is_none(Diamond.Parse("diabc"))
        assert_is_none(Diamond.Parse("di3.5"))

    def testOctagon(self):
        assert_equal(Octagon(60., 60., 20.), Octagon.Parse("oct60x60x20"))
        assert_equal(Octagon(60., 30., 20.), Octagon.Parse("oct60x30x20"))
        assert_equal(Octagon(1., 2.0, 3.0), Octagon.Parse("oct1.0x2.0x3.0"))
        assert_equal(Octagon(5.1, 3.33, 61.2), Octagon.Parse("oct5.1x3.33x61.2"))
        assert_is_none(Octagon.Parse("oct60x60"))
        assert_is_none(Octagon.Parse("oval3.5"))

    def testRoundDonut(self):
        assert_equal(RoundDonut(60, 30), RoundDonut.Parse("donut_r60x30"))
        assert_equal(RoundDonut(3.5, 2.5), RoundDonut.Parse("donut_r3.5x2.5"))
        assert_is_none(RoundDonut.Parse("donut1x2"))
        assert_is_none(RoundDonut.Parse("r3.5"))
        assert_is_none(RoundDonut.Parse("donut_r1x2x3"))

    def testSquareDonut(self):
        assert_equal(SquareDonut(60, 30), SquareDonut.Parse("donut_s60x30"))
        assert_equal(SquareDonut(3.5, 2.5), SquareDonut.Parse("donut_s3.5x2.5"))
        assert_is_none(SquareDonut.Parse("donut_r1x2"))
        assert_is_none(SquareDonut.Parse("r3.5"))
        assert_is_none(SquareDonut.Parse("donut_s1x2x3"))

    def testSquareRoundDonut(self):
        assert_equal(SquareRoundDonut(60, 30), SquareRoundDonut.Parse("donut_sr60x30"))
        assert_equal(SquareRoundDonut(3.5, 2.5), SquareRoundDonut.Parse("donut_sr3.5x2.5"))
        assert_is_none(SquareRoundDonut.Parse("donut_r1x2"))
        assert_is_none(SquareRoundDonut.Parse("r3.5"))
        assert_is_none(SquareRoundDonut.Parse("donut_s1x2x3"))

