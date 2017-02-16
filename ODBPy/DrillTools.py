#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read the structured text ODB++ drill tools file
"""
import gzip
from collections import namedtuple, defaultdict
import os.path
from enum import Enum
from .Utils import readFileLines 
from .StructuredTextParser import read_structured_text
from .Structures import HolePlating

__all__ = ["DrillToolSet", "DrillTool", "DrillToolType", "parse_drill_tools", "read_drill_tools"]

DrillToolSet = namedtuple("DrillToolSet", ["metadata", "tools"])
DrillTool = namedtuple("DrillTool", ["num", "type", "tooltype", "size", "info"]) # size in mil

_drill_plating_map = {
    "VIA": HolePlating.Via,
    "NON_PLATED": HolePlating.NonPlated,
    "PLATED": HolePlating.Plated
}

class DrillToolType(Enum):
    """Drill tool type, i.e the TYPE2 field of the tools file"""
    Standard = 1
    Photo = 2
    Laser = 3
    PressFit = 4

_drill_tool_type_map = {
    "STANDARD": DrillToolType.Standard,
    "PHOTO": DrillToolType.Photo,
    "LASER": DrillToolType.Laser,
    "PRESS_FIT": DrillToolType.PressFit
}

def structured_array_to_drill_tool(array):
    if array.name not in ["TOOL", "TOOLS"]:
        raise ValueError("Array {} does not have TOOLS name but {}".format(
            array, array.name))
    info = {
        k: v for k, v in array.attributes.items()
        # Remove keys which are used in the tool directly
        if k not in ["NUM", "TYPE", "DRILL_SIZE", "TYPE2"]
    }
    return DrillTool(array.attributes["NUM"],
                     _drill_plating_map[array.attributes["TYPE"]],
                     _drill_tool_type_map[array.attributes["TYPE2"]],
                     array.attributes["DRILL_SIZE"], info)

def parse_drill_tools(structured_text):
    """Parse a DrillToolSet from a StructuredText set"""
    metadata, arrays = structured_text
    tools = (structured_array_to_drill_tool(array) for array in arrays)
    toolmap = {
        tool.num: tool for tool in tools
    }
    return DrillToolSet(metadata, toolmap)

def read_drill_tools(odbpath):
    "Read the drill tools from a given ODB++ directory"
    stext = read_structured_text(os.path.join(odbpath, "steps/pcb/layers/through_drill/tools"))
    return parse_drill_tools(stext)
