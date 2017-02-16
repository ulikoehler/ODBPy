#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_false, raises, assert_is_none
from ODBPy.SurfaceParser import *
from ODBPy.Structures import *
from ODBPy.Decoder import *

class TestSurfaceParser(object):

    def test_parse_sb(self):
        assert_equal(SurfaceBeginTag(Polarity.Positive, 0, {}),
            run_decoder_on_line("S P 0", surface_decoder_options))
        assert_equal(SurfaceBeginTag(Polarity.Negative, 0, {}),
            run_decoder_on_line("S N 0", surface_decoder_options))
        assert_equal(SurfaceBeginTag(Polarity.Positive, 1, {}),
            run_decoder_on_line("S P 1", surface_decoder_options))
        assert_equal(SurfaceBeginTag(Polarity.Positive, 1, {3:5}),
            run_decoder_on_line("S P 1;3=5", surface_decoder_options))
        assert_equal(SurfaceBeginTag(Polarity.Positive, 1, {3:5}),
            run_decoder_on_line("S P 1 ; 3=5", surface_decoder_options))

        assert_is_none(run_decoder_on_line("SB P 1 2", surface_decoder_options))
