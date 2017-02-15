#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ line decoder

Lazily lines, usually from line record files,
into tag lists.

The result can then be used in the treeifier.
"""
from collections import namedtuple

__all__ = ["run_decoder", "DecoderOption"]

class DecoderOption(namedtuple("DecoderOption", ["regex", "function"])):
    """
    A regex that might match a line and a function to process
    the match into a tag process. The function is unary and takes only the match
    """
    def run(self, line):
        """
        Run the decoder option on a string (using re search).
        Returns function(match) if there is a match and None else
        """
        match = self.regex.search(line)
        return self.function(match) if match is not None else None

def _run_decoder_on_line(line, opts):
    """
    Run a decoder on a line and return a tag or None
    """
    potential_matches = (opt.run(line) for opt in opts)
    # Remove Nones from generator
    matches = filter(lambda x: x is not None, potential_matches)
    try:
        return next(matches)
    except StopIteration:
        return None

def run_decoder(lines, opts):
    return (_run_decoder_on_line(line, opts) for line in lines)
