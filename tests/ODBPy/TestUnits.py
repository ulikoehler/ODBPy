#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from nose.tools import assert_equal, assert_true, assert_almost_equal, assert_false, raises, assert_is_none
from ODBPy.Units import *

class TestUnits(object):
    def test_to_mm(self):
        assert_almost_equal(25.4, to_mm(1.0, "in"))
        assert_almost_equal(25.4, to_mm(1.0, "In"))
        assert_almost_equal(25.4, to_mm(1.0, "iN"))
        assert_almost_equal(25.4, to_mm(1.0, "IN"))
        assert_almost_equal(25.4, to_mm(1.0, "INCH"))
        assert_almost_equal(25.4, to_mm(1.0, "inch"))
        assert_almost_equal(25.4, to_mm(1000.0, "mil"))
        assert_almost_equal(0.0254, to_mm(1, "mil"))
        assert_almost_equal(0.0, to_mm(0.0, "inch"))

    def test_to_mil(self):
        assert_almost_equal(39.3701, to_mil(1.0, "mm"), 4)
        assert_almost_equal(1000., to_mil(1.0, "in"), 4)
        assert_almost_equal(1., to_mil(1.0, "mil"), 4)
        assert_almost_equal(0.0393701, to_mil(1.0, "um"), 4)

    def test_to_um(self):
        assert_almost_equal(25.4, to_micrometers(1.0, "mil"))
        assert_almost_equal(25400, to_micrometers(1.0, "inch"))

    def test_to_inch(self):
        assert_almost_equal(0.0393701, to_inch(1.0, "mm"), 4)
        assert_almost_equal(1., to_inch(1.0, "in"), 4)
        assert_almost_equal(0.001, to_inch(1.0, "mil"), 4)
        assert_almost_equal(0.0000393701, to_inch(1.0, "um"), 4)

    def test_linerecords_unit(self):
        assert_equal("MM", linerecords_unit({"Units": ["U MM"]}))

    @raises(ValueError)
    def test_linerecords_unit_toomany(self):
        assert_equal("MM", linerecords_unit({"Units": ["U MM", "U IN"]}))

    @raises(ValueError)
    def test_linerecords_unit_wrongformat(self):
        assert_equal("MM", linerecords_unit({"Units": ["UBAR"]}))
