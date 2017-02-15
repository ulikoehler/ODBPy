#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, raises, assert_is_none
from ODBPy.StandardSymbols import *

class TestStandardSymbolParsing(object):
    def testRound(self):
        assert_equal(Round(3.5), Round.Parse("r3.5"))
        assert_is_none(Round.Parse("rabc"))
