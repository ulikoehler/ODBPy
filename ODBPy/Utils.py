#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
from zipfile import ZipFile

__all__ = ["readFileLines", "readGZIPFileLines", "readZIPFileLines", "try_parse_number",
           "not_none", "const_false"]

def try_parse_number(s):
    """
    Return int(s), float(s) or s if unparsable.
    Also returns s if s starts with 0 unless it is "0" or starts with "0."
    (and therefore can't be treated like a number)
    """
    if s.startswith("0") and len(s) != 1 and not s.startswith("0."):
        return s
    # Try parsing a nmeric
    try:
        return int(s)
    except ValueError: # Try float or return s
        try:
            return float(s)
        except:
            return s

def readFileLines(filepath, open_fn=open):
    "Get stripped lines of a given file"
    try: # Assume file-like object
        return [l.strip() for l in filepath.read().split("\n")]
    except AttributeError:
        with open_fn(filepath) as fin:
            return [l.strip() for l in fin.read().split("\n")]

def readGZIPFileLines(filepath):
    "Get stripped lines of a given file in gzip format"
    return readFileLines(filepath, open_fn=gzip.open)

def readZIPFileLines(filepath, codec="utf-8"):
    "Get stripped lines of a given ZIP file containing only one entry"
    with ZipFile(filepath, 'r') as thezip:
        names = thezip.namelist()
        if len(names) != 1:
            raise ValueError("ZIP files does not contain exactly one file: {}".format(names))
        return [l.strip() for l in
                thezip.read(names[0]).decode(codec).split("\n")]

def not_none(x):
    "Return True exactly if x is not None. Mostly used as a filter predicate."
    return x is not None

def const_false():
    "Always return False. Used in place of a lambda."
    return False
