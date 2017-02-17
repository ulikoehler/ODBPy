#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ layer feature parser.

Parses features like pads and lines from 
"""
from collections import namedtuple
from .Decoder import DecoderOption, run_decoder
from .Structures import Mirror, Point, polarity_map
from .Attributes import parse_attributes
from .Structures import SymbolReference
import re

# See http://www.odb-sa.com/wp-content/uploads/ODB_Format_Description_v7.pdf p. 112
_pad_re = re.compile(r"^P\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(\d+|-1\s+\d+\s+-?[\.\d]+)\s+([PN])\s+(\d+)\s+([1-7]|[8-9]\s+-?[\.\d]+)(;\s*.+?)?$")
# _pad_re.match('P -35.7225 2.064 0 P 0 8 0;0=2,1=0')
_line_re = re.compile(r"^L\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(\d+)\s+([PN])\s+(\d+)(;\s*.+?)?$")

Pad = namedtuple("Pad", ["coords", "symbol", "polarity", "dcode", "mirror", "angle", "attributes"])
Line = namedtuple("Line", ["start", "end", "symbol", "polarity", "dcode", "attributes"])

_orientation_old_to_new_lut = {
    0: "8 0",
    1: "8 90",
    2: "8 180",
    3: "8 270",
    4: "9 0",
    5: "9 90",
    6: "9 180",
    7: "9 270"
}

_orientation_mirror_lut = { # Old values are converted to 8 or 9
    8: Mirror.No,
    9: Mirror.MirrorX
}

def _parse_line(match):
    "Parse a line regex match"
    xs, ys, xe, ye, symnum, polarity, dcode, attributes = match.groups()
    return Line(Point(float(xs), float(ys)), Point(float(xe), float(ye)),
                SymbolReference(symnum, 1.0), polarity_map[polarity],
                int(dcode), attributes)

def _parse_pad(match):
    "Parse a pad regex match"
    x, y, apt_def, polarity, dcode, orient_def, attributes = match.groups()
    # If the short syntax for apt_def is used, convert it to the long syntax
    if " " not in apt_def:
        apt_def = "-1 {0} 1.0".format(apt_def)
    _, sym, resize_factor = apt_def.split()
    aptref = SymbolReference(int(sym), float(resize_factor))
    # Convert old rotation syntax to new syntax
    if " " not in orient_def:
        orient_def = _orientation_old_to_new_lut[int(orient_def)]
    orient_code, orient_angle = orient_def.split()
    orient_code = int(orient_code)
    orient_angle = float(orient_angle)
    mirror = _orientation_mirror_lut[orient_code]
    # Parse attributes
    attributes = parse_attributes(attributes[1:]) \
                 if attributes is not None else {}
    # Create return object
    return Pad(Point(float(x), float(y)),
               aptref, polarity_map[polarity],
               int(dcode), mirror, orient_angle, attributes)


_features_decoder_options = [
    DecoderOption(_pad_re, _parse_pad),
    DecoderOption(_line_re, _parse_line)
]

def decode_features(linerecords):
    features = run_decoder(linerecords["Layer features"], _features_decoder_options)
    return features

#_pad_re.match("P 1.0 2.0 -1 0 0.02 P 4 8 30.0").groups()
#_parse_pad(_pad_re.match(s))
