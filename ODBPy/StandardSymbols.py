#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ standard symbol geometries
"""
import re
from enum import Enum
from collections import namedtuple

# See ODB++ 7.0 spec page 202
class Round(namedtuple("Round", ["diameter"])):
    regex = re.compile(r"r[\.\d]+")

    @staticmethod
    def Parse(s):
        match = Round.regex.match(s)
        if match is None:
            return None
        return Round(float(match.group(1)))


Square = namedtuple("Square", ["side"])
Rectangle = namedtuple("Rectangle", ["width", "height"])
# TODO: Rounded and chamfered rectangle currently not supported
Oval = namedtuple("Oval", ["width", "height"])
Diamond = namedtuple("Diamond", ["width", "height"])
Octagon = namedtuple("Octagon", ["width", "height", "corner_size"])
RoundDonut = namedtuple("RoundDonut", ["outer_diameter", "inner_diameter"])
SquareDonut = namedtuple("SquareDonut", ["outer_diameter", "inner_diameter"])
# New in v7.0
SquareRoundDonut = namedtuple("SquareRoundDonut", ["outer_diameter", "inner_diameter"])
RoundedSquareDonut = namedtuple("RoundedSquareDonut", ["outer_diameter", "inner_diameter", "corner_radius", "corners"])
RectangleDonut = namedtuple("RectangleDonut", ["outer_width", "outer_height", "line_width"])
RoundedRectangleDonut = namedtuple("RoundedRectangleDonut", ["outer_width", "outer_height", "line_width", "corner_radius", "corners"])
OvalDonut = namedtuple("OvalDonut", ["outer_width", "outer_height", "line_width"])

HorizontalHexagon = namedtuple("HorizontalHexagon", ["width", "height", "corner_size"])
VerticalHexagon = namedtuple("VerticalHexagon", ["width", "height", "corner_size"])

Butterfly = namedtuple("Butterfly", ["diameter"])
SquareButterfly = namedtuple("SquareButterfly", ["size"])

Triangle = namedtuple("Triangle", ["base", "height"])
HalfOval = namedtuple("HalfOval", ["width", "height"])

RoundThermalRounded = namedtuple("RoundThermalRounded", ["outer_diameter", "inner_diameter", "angle", "num_spokes", "gap"])
RoundThermalSquared = namedtuple("RoundThermalSquared", ["outer_diameter", "inner_diameter", "angle", "num_spokes", "gap"])
SquareThermal = namedtuple("SquareThermal", ["outer_size", "inner_size", "angle", "num_spokes", "gap"])
SquareThermalOpenCorners = namedtuple("SquareThermalOpenCorners", ["outer_diameter", "inner_diameter", "angle", "num_spokes", "gap"])
SquareRoundThermal = namedtuple("SquareRoundThermal", ["outer_size", "inner_diameter", "angle", "num_spokes", "gap"])
RectangularThermal = namedtuple("RectangularThermal", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "air_gap"])
RectangularThermalOpenCorners = namedtuple("RectangularThermalOpenCorners", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "air_gap"])
RoundedSquareThermal = namedtuple("RoundedSquareThermal", ["outer_size", "inner_size", "angle", "num_spokes", "gap", "corner_radius", "corners"])
RoundedSquareThermalOpenCorners = namedtuple("RoundedSquareThermalOpenCorners", ["outer_diameter", "inner_diameter", "angle", "num_spokes", "gap", "rad", "corners"])
RoundedRectangleThermal = namedtuple("RoundedRectangleThermal", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "corner_radius", "corners"])
RoundedRectangleThermalOpenCorners = namedtuple("RoundedRectangleThermalOpenCorners", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "corner_radius", "corners"])
OvalThermal = namedtuple("OvalThermal", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "line_width"])
OvalThermalOpenCorners = namedtuple("OvalThermalOpenCorners", ["outer_width", "outer_height", "angle", "num_spokes", "gap", "line_width"])

Ellipse = namedtuple("Ellipse", ["width", "height"])

Moire = namedtuple("Moire", ["ring_width", "ring_gap", "num_rings", "line_width", "line_length", "line_angle"])


class HolePlating(Enum):
    Plated = 1
    NonPlated = 2
    Via = 3

Hole = namedtuple("Hole", ["diameter", "plating", "tolerance_plus", "tolerance_minus"])
