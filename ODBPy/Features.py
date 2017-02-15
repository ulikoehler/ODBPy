#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ODB++ feature info parser
"""
from collections import namedtuple

__all__ = ["FeatureInfo", "parse_feature_info"]

class FeatureInfo(namedtuple("FeatureInfo", ["symbol_names", "attribute_names", "strings"])):
    def apply(self, attributes):
        """Apply the current feature info to a given attribute dictionary.
        This function is not content-aware and therefore"""
        return {
            self.attribute_names[k]: v
            for k, v in attributes.items()
        }

def parse_feature_map(elems):
    # The first character ($, @, &) is ignored as it is clear from the context
    ret = {}
    for elem in elems:
        k, _, v = elem.partition(" ")
        ret[int(k[1:])] = v
    return ret

def parse_feature_info(linerecords):
    return FeatureInfo (
        parse_feature_map(linerecords["Feature symbol names"]),
        parse_feature_map(linerecords["Feature attribute names"]),
        parse_feature_map(linerecords["Feature attribute text strings"])
    )
