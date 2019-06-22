#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ common data structures
"""
from collections import namedtuple
from enum import Enum
import numbers

__all__ = ["Point", "Polarity", "polarity_map", "Mirror",
           "mirror_map", "HolePlating", "SymbolReference"]

# Named tuples
class Point(namedtuple("Point", ["x", "y"])):
    """
    Represents a X/Y point in the 2D ODB++ plane.
    The units and reference of the coordinate need to be
    interpreted according to context.
    """
    def __add__(self, op):
        if isinstance(op, numbers.Number):
            return Point(self.x + op, self.y + op)
        if isinstance(op, Point):
            return Point(self.x + op.x, self.y + op.y)

    def __sub__(self, op):
        if isinstance(op, numbers.Number):
            return Point(self.x - op, self.y - op)
        if isinstance(op, Point):
            return Point(self.x - op.x, self.y - op.y)

    def __mul__(self, op):
        if isinstance(op, numbers.Number):
            return Point(self.x * op, self.y * op)
        if isinstance(op, Point):
            return Point(self.x * op.x, self.y * op.y)

    def __truediv__(self, op):
        if isinstance(op, numbers.Number):
            return Point(self.x / op, self.y / op)
        if isinstance(op, Point):
            return Point(self.x / op.x, self.y / op.y)
# Enums
class Polarity(Enum):
    """Polarity of a layer"""
    Positive = 1
    Negative = 2

polarity_map = {
    "P": Polarity.Positive,
    "POSITIVE": Polarity.Positive,
    "N": Polarity.Negative,
    "NEGATIVE": Polarity.Negative
}

class Mirror(Enum):
    """Mirror settings"""
    No = 1
    Mirror = 2 # Unspecific mirroring
    MirrorX = 3
    MirrorY = 4
    MirrorXY = 5

mirror_map = {
    "N": Mirror.No,
    "M": Mirror.Mirror,
    "Y": Mirror.MirrorY,
    "X": Mirror.MirrorX,
    "XY": Mirror.MirrorXY,
}

class HolePlating(Enum):
    """The plating status for a drilled hole"""
    Plated = 1
    NonPlated = 2
    Via = 3

_SymbolReference = namedtuple("SymbolReference", ["symcode", "resize_factor"])

class SymbolReference(_SymbolReference):
    """
    A numeric reference to a symbol stored elsewhere,
    with an optional resize factor
    """
    def __init__(self, symnum, resize_factor=1.0):
            _SymbolReference.__init__(symnum, resize_factor)
