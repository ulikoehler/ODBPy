#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ standard symbol geometries
See ODB++ 7.0 spec page 202++
"""
import re
from enum import Enum
from collections import namedtuple
import functools

def _parse_allfloat(rgx, constr, s):
    """
    Parse a string using a regex yielding only floats group
    """
    match = rgx.match(s)
    if match is None:
        return None
    return constr(*map(float, match.groups()))

def _parse_allfloat_corners(rgx, constr, s):
    """
    Parse a string using a regex yielding only floats group,
    with the exception of the last group, being an optional corner
    group containing a list of corners
    """
    match = rgx.match(s)
    if match is None:
        return None
    groups = match.groups()
    # Treat last group separately
    cornersStr = groups[-1] if groups[-1] is not None else "1234"
    corners = [int(c) for c in cornersStr if c.isdigit()]
    # Assemble args list
    args = list(map(float, groups[:-1]))
    args.append(corners)
    print(args)
    return constr(*args)


def _standard_symbol_factory(name, regex, field_names, parsefunc):
    """
    Generates a new standard symbol container class
    (derived from namedtuple) from a matcher regex,
    a list of fields and one of the _parse_... parsers
    from this module
    """
    _cls = namedtuple(name, field_names)
    _cls.regex = re.compile(regex)
    _cls.Parse = functools.partial(parsefunc, _cls.regex, _cls)
    return _cls

Round = _standard_symbol_factory("Round", r"^r([\.\d]+)$", ["diameter"], _parse_allfloat)
Square = _standard_symbol_factory("Square", r"^s([\.\d]+)$", ["side"], _parse_allfloat)

Rectangle = _standard_symbol_factory("Rectangle", r"^r([\.\d]+)x([\.\d]+)$",
    ["width", "height"], _parse_allfloat)

Oval = _standard_symbol_factory("Oval", r"^oval([\.\d]+)x([\.\d]+)$", ["width", "height"], _parse_allfloat)

Diamond = _standard_symbol_factory("Diamond",
    r"^di([\.\d]+)x([\.\d]+)$", ["width", "height"], _parse_allfloat)

Octagon = _standard_symbol_factory("Octagon",
    r"^oct([\.\d]+)x([\.\d]+)x([\.\d]+)$", ["width", "height", "corner_size"], _parse_allfloat)

# TODO: Rounded and chamfered rectangle currently not supported
RoundDonut = _standard_symbol_factory("RoundDonut",
    r"^donut_r([\.\d]+)x([\.\d]+)$", ["outer_diameter", "inner_diameter"], _parse_allfloat)

SquareDonut = _standard_symbol_factory("SquareDonut",
    r"^donut_s([\.\d]+)x([\.\d]+)$", ["outer_diameter", "inner_diameter"], _parse_allfloat)

SquareRoundDonut = _standard_symbol_factory("SquareRoundDonut",
    r"^donut_sr([\.\d]+)x([\.\d]+)$", ["outer_diameter", "inner_diameter"], _parse_allfloat)

RoundedSquareDonut = _standard_symbol_factory("RoundedSquareDonut",
    r"^donut_s([\.\d]+)x([\.\d]+)xr([\.\d]+)(x[\.\d]+)?$",
    ["outer_diameter", "inner_diameter", "corner_radius", "corners"], _parse_allfloat_corners)

RectangleDonut = _standard_symbol_factory("RectangleDonut",
    r"^donut_rc([\.\d]+)x([\.\d]+)x([\.\d]+)$",
    ["outer_diameter", "inner_diameter", "line_width"], _parse_allfloat)

RoundedRectangleDonut = _standard_symbol_factory("RoundedRectangleDonut",
    r"^donut_rc([\.\d]+)x([\.\d]+)x([\.\d]+)xr([\.\d]+)(x[\.\d]+)?$",
    ["outer_diameter", "inner_diameter", "line_width", "corner_radius", "corners"], _parse_allfloat_corners)

OvalDonut = _standard_symbol_factory("OvalDonut",
    r"^donut_o([\.\d]+)x([\.\d]+)x([\.\d]+)$",
    ["outer_diameter", "inner_diameter", "line_width"], _parse_allfloat)

HorizontalHexagon = _standard_symbol_factory("HorizontalHexagon",
    r"^hex_l([\.\d]+)x([\.\d]+)x([\.\d]+)$",
    ["width", "height", "corner_size"], _parse_allfloat)

VerticalHexagon = _standard_symbol_factory("VerticalHexagon",
    r"^hex_s([\.\d]+)x([\.\d]+)x([\.\d]+)$",
    ["width", "height", "corner_size"], _parse_allfloat)

Butterfly = _standard_symbol_factory("Butterfly",
    r"^bfr([\.\d]+)$", ["diameter"], _parse_allfloat)

SquareButterfly = _standard_symbol_factory("SquareButterfly",
    r"^bfs([\.\d]+)$", ["size"], _parse_allfloat)

Triangle = _standard_symbol_factory("Triangle",
    r"^tri([\.\d]+)x([\.\d]+)$", ["base", "height"], _parse_allfloat)

HalfOval = _standard_symbol_factory("HalfOval",
    r"^oval_h([\.\d]+)x([\.\d]+)$", ["width", "height"], _parse_allfloat)


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
