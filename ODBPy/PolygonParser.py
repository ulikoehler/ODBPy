#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ polygon parser components
"""
import re
from collections import namedtuple
from enum import Enum
from .Structures import Point
from .Decoder import DecoderOption
from .Treeifier import TreeifierRule

__all__ = ["Polygon", "PolygonSegment", "PolygonCircle",
           "PolygonBeginTag", "PolygonSegmentTag", "PolygonCircleTag", "PolygonEndTag",
           "PolygonType", "CircleDirection", "polygon_decoder_options",
           "polygon_treeify_rules"]

# Polygon steps consist of PolygonSegment and PolygonCircle objects
class Polygon(namedtuple("Polygon", ["type", "steps"])):
    def min(self):
        """Returns (minimum x, minimum y) of both coordinates"""
        return Point(min(step.min()[0] for step in self.steps), min(step.min()[1] for step in self.steps))
    def max(self):
        """Returns (maximum x, maximum y) of both coordinates"""
        return Point(max(step.max()[0] for step in self.steps), max(step.max()[1] for step in self.steps))


class PolygonSegment(namedtuple("PolygonSegment", ["start", "end"])):
    def min(self):
        """Returns (minimum x, minimum y) of both coordinates"""
        return Point(min(self.start.x, self.end.x), min(self.start.y, self.end.y))
    def max(self):
        """Returns (maximum x, maximum y) of both coordinates"""
        return Point(max(self.start.x, self.end.x), max(self.start.y, self.end.y))

PolygonCircle = namedtuple("PolygonCircle", ["start", "end", "center", "direction"])

PolygonBeginTag = namedtuple("PolygonBeginTag", ["start", "type"])
PolygonSegmentTag = namedtuple("PolygonSegmentTag", ["end"])
PolygonCircleTag = namedtuple("PolygonCircleTag", ["end", "center", "direction"])
PolygonEndTag = namedtuple("PolygonEndTag", [])

# Enums
class PolygonType(Enum):
    """Type of a polygon"""
    Island = 1
    Hole = 2

_polygon_type_map = {
    "I": PolygonType.Island,
    "H": PolygonType.Hole
}

class CircleDirection(Enum):
    """Direction of a circle in a polygon"""
    Clockwise = 1
    CounterClockwise = 2
    
_circle_direction_map = {
    "Y": CircleDirection.Clockwise,
    "N": CircleDirection.CounterClockwise
}

# Regular expressions for contour syntax
_ob_re = re.compile(r"^OB\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+([IH])")
_os_re = re.compile(r"^OS\s+(-?[\.\d]+)\s+(-?[\.\d]+)")
_oc_re = re.compile(r"^OC\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+([YN])")
_oe_re = re.compile(r"^OE\s*$")

def _parse_os(match):
    "Parse a polynom segment tag regex match"
    x, y = match.groups()
    return PolygonSegmentTag(Point(float(x), float(y)))

def _parse_oc(match):
    "Parse a polynom circle tag regex match"
    xe, ye, xc, yc, cw = match.groups()
    return PolygonCircleTag(Point(float(xe), float(ye)),
                            Point(float(xc), float(yc)),
                            _circle_direction_map[cw])

def _parse_oe(match):
    "Parse a polynom end tag regex match"
    return PolygonEndTag()

def _parse_ob(match):
    "Parse a polynom begin tag regex match"
    x, y, ptype = match.groups()
    return PolygonBeginTag(Point(float(x), float(y)),
                           _polygon_type_map[ptype]) # Empty step list

polygon_decoder_options = [
    DecoderOption(_ob_re, _parse_ob),
    DecoderOption(_os_re, _parse_os),
    DecoderOption(_oc_re, _parse_oc),
    DecoderOption(_oe_re, _parse_oe)
]

def _treeifier_process_polygon(elems):
    """Treeifier processor function for polygons."""
    steps = []
    cur_point, polytype = elems[0] # Poly begin tag
    for elem in elems[1:]: # Iterate everything except the end tag
        if isinstance(elem, PolygonSegmentTag):
            steps.append(PolygonSegment(cur_point, elem.end))
        if isinstance(elem, PolygonCircleTag):
            steps.append(PolygonCircle(
                    cur_point, elem.end, elem.center, elem.direction))
        cur_point = elem.end
    # Build polygon structure
    return Polygon(polytype, steps)

polygon_treeify_rules = [
    TreeifierRule(PolygonBeginTag, PolygonEndTag, _treeifier_process_polygon)
]