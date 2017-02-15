#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser for the ODB++ PCB profile file
"""
import os.path
from .LineRecordParser import *
from .SurfaceParser import *
from .PolygonParser import *
from .Decoder import *
from .Treeifier import *

def parse_profile(directory):
    profile = read_linerecords(os.path.join(directory, "steps/pcb/profile"))
    # Build rulesets
    decoder_options = surface_decoder_options + polygon_decoder_options
    treeifyer_rules = surface_treeify_rules + polygon_treeify_rules

    decoded = list(run_decoder(profile["Layer features"], decoder_options))
    return treeify(decoded, treeifyer_rules)

if __name__ == "__main__":
    #Parse commandline arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The ODB++ directory")
    args = parser.parse_args()
    #Perform check
    print(parse_profile(args.directory))
