#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing routines for the ODB++ line record text format
according to the ODB++ 7.0 specification:

http://www.odb-sa.com/wp-content/uploads/ODB_Format_Description_v7.pdf
"""
from collections import defaultdict
from .Utils import readFileLines, readZIPFileLines

def filter_line_record_lines(lines):
    "Remove empty and '#'-only lines from the given line list"
    return [
        line for line in lines
        if line and line != "#"
    ]

def read_raw_linerecords(filename):
    "Read a .Z line record file and return only important lines in order"
    open_fn = readZIPFileLines if filename.endswith(".Z") else readFileLines
    return filter_line_record_lines(
        open_fn(filename))

def group_by_section(lines):
    "Group a line record file by the section. Returns a dict containing lists."
    groups = defaultdict(list)
    name = None
    for line in lines:
        if line.startswith("#"):
            name = line.strip("#").strip()
        else:
            groups[name].append(line)
    return dict(groups)

def read_linerecords(filename):
    "Read a linerecord file and return a dict grouped by section"
    return group_by_section(read_raw_linerecords(filename))
