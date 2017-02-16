#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ attribute parser
"""

__all__ = ["parse_attributes_from_line",
           "parse_attributes"]

def parse_attributes_from_line(line):
    """
    Given a pre-stripped line from a line record file,
    parse the attribute section.
    Returns a dict of numeric attribute values.

    Example:
        parse_attributes_from_line("P -30.9595 3.8107 0 P 0 8 0;0=0,2=0") => {0: 0, 2: 0}
    """
    attribute_str = line.partition(";")[2].strip()
    return parse_attributes(attribute_str) if attribute_str else {}

def parse_attributes(attribute_str):
    """
    Given the attribute part from a line record file,
    parse the attribute section.
    Returns a dict of numeric attribute values.

    Example:
        parse_attributes("0=0,2=0") => {0: 0, 2: 0}
    """
    # Split into individual key/value pairs
    attrs = (s.strip() for s in attribute_str.split(","))
    # Split each k/v pair into individual parts
    part_attrs = (
        attr.partition("=") if "=" in attr else (attr, None, True)
        for attr in attrs)
    # Create dict of ints
    return {
        int(attr[0]): int(attr[2]) if not isinstance(attr[2], bool) else attr[2]
        for attr in part_attrs
    }