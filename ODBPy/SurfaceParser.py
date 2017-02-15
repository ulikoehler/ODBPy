#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ surface parser components
"""
import re
from collections import namedtuple
from .Decoder import DecoderOption
from .Treeifier import TreeifierRule
from .PolygonParser import Polygon
from .Structures import Polarity, polarity_map

__all__ = ["surface_decoder_options",
           "SurfaceBeginTag", "surface_treeify_rules",
           "surface_decoder_options",
           "SurfaceEndTag", "Surface", "Polarity"]

Surface = namedtuple("Surface", ["polarity", "dcode", "polygons", "attributes"])

SurfaceBeginTag = namedtuple("SurfaceBeginTag", ["polarity", "dcode", "attributes"])
SurfaceEndTag = namedtuple("SurfaceEndTag", [])

# Surface syntax regular expressions
_surface_re = re.compile(r"^S\s+([PN])\s+(\d+)\s*(;\s*.+?)?$")
_surface_end_re = re.compile(r"^SE\s*$")

def _parse_surface_start(match):
    "Parse a surface begin tag regex match"
    polarity, dcode, attributes = match.groups()
    # Parse attribute string
    attributes = parse_attributes(attributes[1:]) \
                 if attributes is not None else {}
    return SurfaceBeginTag(polarity_map[polarity],
                           int(dcode), attributes)

def _parse_surface_end(match):
    "Parse a surface end tag regex match"
    return SurfaceEndTag()


surface_decoder_options = [
    DecoderOption(_surface_re, _parse_surface_start),
    DecoderOption(_surface_end_re, _parse_surface_end)
]

def _treeifier_process_surface(elems):
    """Treeifier processor function for surfaces."""
    polygons = []
    polarity, dcode, attributes = elems[0] # Poly begin tag
    for elem in elems[1:]: # Iterate everything except the end tag
        if isinstance(elem, Polygon):
            polygons.append(elem)
    # Build polygon structure
    return Surface(polarity, dcode, polygons, attributes)


surface_treeify_rules = [
    TreeifierRule(SurfaceBeginTag, SurfaceEndTag, _treeifier_process_surface),
]
