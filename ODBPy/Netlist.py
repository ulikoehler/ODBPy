#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing routines for the ODB++ netlist format
according to the ODB++ 7.0 specification:

http://www.odb-sa.com/wp-content/uploads/ODB_Format_Description_v7.pdf
"""
from .Decoder import run_decoder
import functools
from toolz.itertoolz import groupby
import operator
import os.path
from .LineRecordParser import read_linerecords
from .Utils import not_none
from .NetlistParser import netlist_decoder_options, assign_net_name, parse_net_names

__all_ = ["read_netlist"]


def read_netlist(directory):
    netlist_path = os.path.join(directory, "steps/pcb/netlists/cadnet/netlist")
    linerec = read_linerecords(netlist_path)
    netnames = parse_net_names(linerec)
    # All the following operations are performed lazily
    decoded = run_decoder(linerec["Netlist points"], netlist_decoder_options)
    decoded = filter(not_none, decoded)
    decoded_mapped = map(functools.partial(assign_net_name, netnames), decoded)
    return groupby(operator.attrgetter("netid"), decoded_mapped)

if __name__ == "__main__":
    #Parse commandline arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The ODB++ directory")
    args = parser.parse_args()
    #Perform check
    print(read_netlist(args.directory))
