#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser for the ODB++ PCB profile file
"""
import os.path
from collections import namedtuple
from .LineRecordParser import *
from .SurfaceParser import *
from .PolygonParser import *
from .Decoder import *
from .Treeifier import *
from .Units import *

__all__ = ["read_profile", "parse_profile", "Profile"]

Profile = namedtuple("Profile", ["unit", "surfaces"])

def read_profile(directory):
    profile = read_linerecords(os.path.join(directory, "steps/pcb/profile"))
    return parse_profile(profile)

def parse_profile(linerecords):
    # Build rulesets
    decoder_options = surface_decoder_options + polygon_decoder_options
    treeifyer_rules = surface_treeify_rules + polygon_treeify_rules

    decoded = list(run_decoder(linerecords["Layer features"], decoder_options))
    surfaces = treeify(decoded, treeifyer_rules)
    return Profile(linerecords_unit(linerecords), surfaces)
