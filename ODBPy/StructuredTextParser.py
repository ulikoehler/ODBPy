#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parsing routines for the ODB++ structured text format
according to the ODB++ 7.0 specification:

http://www.odb-sa.com/wp-content/uploads/ODB_Format_Description_v7.pdf
"""
from collections import defaultdict, namedtuple
import os.path
import re
from .Utils import readFileLines, try_parse_number

__all__ = ["StructuredArray", "StructuredText", "parse_structured_text", "read_structured_text"]

StructuredText = namedtuple("StructuredText", ["metadata", "arrays"])
StructuredArray = namedtuple("StructuredArray", ["name", "attributes"])
array_start_re = re.compile(r"(\w+)\s+\{")


def read_structured_text(filename):
    "Run parse_structured_text() on the content of the given file"
    return parse_structured_text(readFileLines(filename))

def parse_structured_text(lines):
    """
    Parse structured text lines into a metadata dictionary
    and a set of StructuredArrays.
    Takes a generator of list of pre-stripped lines
    """
    metadata = {}
    arrays = []
    current_array = None
    for line in lines:
        line = line.strip()
        # Parse key/value line
        if "=" in line:
            k, _, v = line.partition("=")
            if current_array is None:
                metadata[k] = try_parse_number(v)
            else:
                current_array.attributes[k] = try_parse_number(v)
            continue
        elif line == "}":
            if current_array is not None:
                arrays.append(current_array)
            current_array = None
            continue
        # Try to parse the start line of an array (e.g. "TOOLS {")
        array_start_match = array_start_re.match(line)
        if array_start_match is not None:
            current_array = StructuredArray(
                array_start_match.group(1), {})
    # Append last tool, if any
    if current_array is not None:
        arrays.append(current_array)
    return StructuredText(metadata, arrays)

if __name__ == "__main__":
    #Parse commandline arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="The structured text file to red")
    args = parser.parse_args()
    #Perform check
    print(read_structured_text(args.file))
