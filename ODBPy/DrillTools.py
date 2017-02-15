#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Read the structured text ODB++ drill tools file
"""
import gzip
from collections import namedtuple, defaultdict
import os.path
from Utils import readFileLines 
from StructuredTextParser import read_structured_text

__all__ = ["DrillToolSet", "DrillTool", "parse_drill_tools", "read_drill_tools"]

DrillToolSet = namedtuple("DrillToolSet", ["metadata", "tools"])
DrillTool = namedtuple("DrillTool", ["num", "type", "size", "info"]) # size in mil

def structured_array_to_drill_tool(array):
    if array.name not in ["TOOL", "TOOLS"]:
        raise ValueError("Array {} does not have TOOLS name but {}".format(
            array, array.name))
    info = {
        k: v for k, v in array.attributes.items()
        # Remove keys which are used in the tool directly
        if k not in ["NUM", "TYPE", "DRILL_SIZE"]
    }
    return DrillTool(array.attributes["NUM"],
                     array.attributes["TYPE"],
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

if __name__ == "__main__":
    #Parse commandline arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The ODB directory")
    args = parser.parse_args()
    #Perform check
    toolset = read_drill_tools(args.directory)
    print("Metadata:")
    for k, v in toolset.metadata.items():
        print("\t{} = {}".format(k, v))

    print("\nTools:")
    for tool in toolset.tools.values():
        print("\t{}".format(tool))
