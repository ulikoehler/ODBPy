#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing routines for the ODB++ netlist format
according to the ODB++ 7.0 specification:

http://www.odb-sa.com/wp-content/uploads/ODB_Format_Description_v7.pdf
"""
import re
from collections import namedtuple, defaultdict
from .Utils import const_false, not_none, try_parse_number
from .Structures import Point
from enum import Enum
from .Decoder import DecoderOption

__all__ = ["is_netlist_optimized", "parse_net_names", "StaggeringParameters",
           "NetlistPointTypeInformation", "NetlistPoint", "TestpointTestSide",
           "NetSide", "NetPointLocation", "NetPointExposure",
           "netlist_decoder_options", "assign_net_name"]

_h_optimize_re = re.compile(r"^H\s+optimize\s+([YN])\s*$", re.IGNORECASE)

# TODO comment point is not supported as the exact format is not clear
_netlist_point_re = re.compile(r"^(-?\d+|\$NONE\$)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+(-?[\.\d]+)\s+([TDB])\s+(-?[\.\d]+\s+-?[\.\d]+)?\s*([em])\s+([ecps])\s+(staggered\s+-?[\.\d]+\s+-?[\.\d]+\s+-?[\.\d]+)?\s*([vV]\s+)?([fF]\s+)?([tT]\s+)?([mM]\s*)?(eXtended\s+\S+\s*)?([csban])?")
# Test cases:
# Actual
# 10 0.0236 0.45 -1.2916 B e e staggered 0 0 0
# 9 0.0069 0.287 -1.312 B e e staggered 0 0 0 v
# 9 0 0.24 -1.18 T 0.0354 0.0276 e e staggered 0 0 0
# Presumed
# TODO
# Testcase format: _parse_netlist_point(_netlist_point_re.search("10 0.0236 0.45 -1.2916 B e e staggered 0 0 0"))


def _generate_boolean_ci_lut(char):
    """
    Generate a boolean result map taking char.lower() and char.upper()
    as True and everything else as False
    """
    ret = defaultdict(const_false)
    ret[char.lower()] = True
    ret[char.upper()] = False
    return ret

_is_via_lut = _generate_boolean_ci_lut("v")
_is_fiducial_lut = _generate_boolean_ci_lut("f")
_is_testpoint_lut = _generate_boolean_ci_lut("t")
_force_midpoint_testable_lut = _generate_boolean_ci_lut("m")


def is_netlist_optimized(linerec):
    """
    Based on a netlist linerecord dict, determines if the netlist
    was optimized by the netlist optimizer.
    Returns bool (True = optimized)
    """
    # Try to look for a regex match in ANY of the lines
    metalines = linerec[None]
    potential_matches = (_h_optimize_re.match(line) for line in metalines)
    matches = filter(not_none, potential_matches)
    try:
        return next(matches).group(1) in ["Y", "y"]
    except StopIteration: # No such line
        raise ValueError("Can't find netlist optimization tag in line record: {}".format(linerec))


def parse_net_names(linerecords):
    """Given a netlist linerecord file, generates a dict of net ID => name mappings"""
    netnames = linerecords["Nets names"]
    splitlines = (line.partition(" ") for line in netnames)
    return {
        int(split[0][1:]): split[2] # [1:]: Throw away $ sign or whatever sign is used
        for split in splitlines
    }


StaggeringParameters = namedtuple("StaggeringParameters", ["location", "radius"])

NetlistPointTypeInformation = namedtuple("NetlistPointTypeInformation", [
        "is_via", "is_fiducial", "is_testpoint", "force_midpoint_testability",
        "extension", "testpoint_testside"
    ])

NetlistPoint = namedtuple("NetlistPoint", [
        "netid", "radius", "location", "side", "size", "point_location",
        "exposure", "staggered", "point_type"])

def _parse_netlist_point(match):
    # netid -1 => tooling hole
    netid, radius, x, y, side, wh, point_location, exposure, staggered, v, f, t, m, xtension, testside = match.groups()
    # wh is only not None when radius is 0 (probably a plated slot)
    if wh is not None:
        w, _, h = wh.partition(" ")
    # Staggered is mostly set for DipTrace exports
    if staggered is not None:
        sx, sy, sr = staggered.split()[1:]
        staggering_params = StaggeringParameters(
            Point(float(sx), float(sy)), float(sr))
    # Extension
    if xtension is not None:
        # Format (presumed): "eXtended foobar"
        # Remove "eXtended"
        xtension = xtension.partition(" ")[2]
    # Create return data structure
    return NetlistPoint(
        try_parse_number(netid),
        float(radius),
        Point(float(x), float(y)),
        _net_side_lut[side],
        Point(float(w), float(h)) if wh is not None else None,
        _net_point_location_lut[point_location],
        _net_point_exposure_lut[exposure],
        staggering_params if staggered is not None else None,
        NetlistPointTypeInformation(
            _is_via_lut[v],
            _is_fiducial_lut[f],
            _is_testpoint_lut[t],
            _force_midpoint_testable_lut[m],
            xtension,
            _testpoint_test_side_lut[testside]
        )
    )


class TestpointTestSide(Enum):
    ComponentSide = 1
    SolderSide = 2
    BothSides = 3
    AnyOneSide = 4
    Undefined = 5

_testpoint_test_side_lut = {
    "c": TestpointTestSide.ComponentSide,
    "s": TestpointTestSide.SolderSide,
    "b": TestpointTestSide.BothSides,
    "a": TestpointTestSide.AnyOneSide,
    "n": TestpointTestSide.Undefined,
    None: TestpointTestSide.Undefined # Spec: Presume "n" if no <by> listed
}

class NetSide(Enum):
    """A netlist side, see ODB++ 7.0 specification page 76"""
    Top = 1
    Bottom = 2
    Both = 3

_net_side_lut = {
    "T": NetSide.Top,
    "D": NetSide.Bottom,
    "B": NetSide.Both
}


class NetPointLocation(Enum):
    EndPoint = 1
    MidPoint = 2

_net_point_location_lut = {
    "e": NetPointLocation.EndPoint,
    "m": NetPointLocation.MidPoint
}

class NetPointExposure(Enum):
    SolderMaskExposed = 1
    SolderMaskCovered = 2
    SolderMaskCoveredPrimaryTop = 3
    SolderMaskCoveredSecondaryBottom = 4

_net_point_exposure_lut = {
    "e": NetPointExposure.SolderMaskExposed,
    "c": NetPointExposure.SolderMaskCovered,
    "p": NetPointExposure.SolderMaskCoveredPrimaryTop,
    "s": NetPointExposure.SolderMaskCoveredSecondaryBottom
}

netlist_decoder_options = [
    DecoderOption(_netlist_point_re, _parse_netlist_point)
]

def assign_net_name(netnames, netpoint):
    """Looksup the netpoint netid in the net name map and replace """
    netid = netpoint.netid
    if netid not in netnames:
        return netpoint
    netname = netnames[netid]
    # Tuples and namedtuples are immutable, so we'll use an intermediary list
    params = list(netpoint)
    params[0] = netname
    return NetlistPoint(*params)
