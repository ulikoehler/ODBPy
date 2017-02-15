#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
= ODB++ AST treefier.

=== Rationale

ODB++ line record file contain structure such as surfaces
that have subelements such as polygons.
The boundaries of those elements are denoted by begin and end tags
comparable to HTML.

The treefier takes the flat tag list and processes it into
a tree of nested lists.

Additionally, every time and end tag is encountered,
the innermost element is processed on the fly.
"""
from collections import namedtuple, deque

__all__ = ["TreeifierRule", "treeify"]

class TreeifierRule(namedtuple("TreeifierRule", ["startcls", "endcls", "function"])):
    """
    A rule for the treefier that idenfies the start and corresponding end element of
    a nested structure.
    
    Once the end tag is encountered, the unary "function" is executed taking
    a list of all tags except the end tag.
    """
    def is_starttag(self, tag):
        return tag.__class__ == self.startcls
    def is_endtag(self, tag):
        return tag.__class__ == self.endcls


def _any_start_rule(tag, rules):
    "Return any rule that has the given tag as a start tag or None"
    try:
        return next(rule for rule in rules if rule.is_starttag(tag))
    except StopIteration:
        return None


def treeify(tags, rules):
    """
    From a flattened list of tag-like objects (i.e. parsed lines) generate a
    nested tree by using start-tag/end-tag rule pairs.
    """
    hierarchy = deque()
    elementlist = deque([[]]) # Contains toplevel element list
    for tag in tags:
        # Check if this is an end tag
        if len(hierarchy) > 0 and hierarchy[-1].is_endtag(tag):
            # Last element of the element list contains the entire previous element
            lst = elementlist.pop()
            # Run processor function on innermost element
            rule = hierarchy.pop()
            elementlist[-1].append(rule.function(lst))
            continue
        # Check if this is an end tag for the current innermost rule
        rule = _any_start_rule(tag, rules)
        if rule is not None:
            hierarchy.append(rule)
            elementlist.append([tag])
            continue
        # Else: It's a free tag
        elementlist[-1].append(tag)
    return elementlist[0]
