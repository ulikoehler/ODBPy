#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parser for the ODB++ PCB matrix file
"""
import os.path
from collections import namedtuple
from .StructuredTextParser import read_structured_text
from .LineRecordParser import read_linerecords
from .Structures import polarity_map
from enum import Enum

__all__ = ["Layer", "LayerSet", "LayerType", "parse_layers", "read_layers",
           "read_layer_components", "read_layer_features"]

class Layer(namedtuple("Layer", ["name", "type", "polarity", "index", "start", "end"])):
    """
    A layer reference in a ODB++ dataset
    start,end = start and end layer name
    """
    def read_features(self, directory):
        """Read the layer feature file for the current layer from the given directory"""
        return read_layer_features(directory, self.name)

    def read_components(self, directory):
        """Read the layer components file for the current layer from the given directory"""
        return read_layer_components(directory, self.name)

class LayerSet(list):
    """
    A list of Layer objects with extra convenience functions
    """
    def by_type(self, layer_type):
        "Find all layers that have the given type"
        return LayerSet(filter(lambda l: l.type == layer_type, self))
    def by_name(self, name):
        "Get a layer by name or None if there is no such layer. Case-insensitive search"
        try:
            name_lower = name.lower()
            return next(filter(lambda l: l.name.lower() == name_lower, self))
        except StopIteration:
            return None

    def component_layers(self):
        """Get all component layers"""
        components = self.by_type(LayerType.Component)
        if len(components) in [2,0]: # Top, bottom or no components
            return components
        elif len(components) == 1:
            layer = components[0]
            # Top or bottom Layer? i.e. is it before or after the 1st signal layer
            first_signal_no = self.signal_layers()[0].index
            return [layer, None] if layer.index < first_signal_no else [None, layer]
        else:
            raise ValueError("Unknown length of component list: {}".format(components))

    def signal_layers(self):
        """Get all signal layers"""
        return self.by_type(LayerType.Signal)

    def top_components(self):
        """Get the top component layer, if any"""
        return self.component_layers()[0]

    def bottom_components(self):
        """Get the top component layer, if any"""
        return self.component_layers()[1]

    def __str__(self):
        return ("LayerSet([\n\t{}\n])".format(
            ",\n\t".join(
                map(str, self))))

class LayerType(Enum):
    Component = 1
    SilkScreen = 2
    SolderPaste = 3
    SolderMask = 4
    Signal = 5
    Drill = 6
    Route = 7
    Document = 8
    Mixed = 9 # Mixed plane & signal
    Mask = 10 # GenFlex additional information
    
_layer_type_map = { # See ODB++ 7.0 spec page 38
    "COMPONENT": LayerType.Component,
    "SILK_SCREEN": LayerType.SilkScreen,
    "SOLDER_PASTE": LayerType.SolderPaste,
    "SOLDER_MASK": LayerType.SolderMask,
    "SIGNAL": LayerType.Signal,
    "DRILL": LayerType.Drill,
    "ROUT": LayerType.Route,
    "DOCUMENT": LayerType.Document,
    "MIXED": LayerType.Mixed,
    "MASK": LayerType.Mask
}

def parse_layers(matrix):
    layers = LayerSet()
    for array in matrix.arrays:
        if array.name != "LAYER":
            continue
        layers.append(Layer(
                array.attributes["NAME"].lower(), # DipTrace seems to use lowercase for directories
                _layer_type_map[array.attributes["TYPE"]],
                polarity_map[array.attributes["POLARITY"]],
                int(array.attributes["ROW"]),
                array.attributes["START_NAME"].lower() or None,
                array.attributes["END_NAME"].lower() or None
        ))
    return layers

def read_layers(directory):
    matrix = read_structured_text(os.path.join(directory, "matrix/matrix"))
    return parse_layers(matrix)

def read_layer_components(directory, layer):
    return read_linerecords(os.path.join(
        directory, "steps", "pcb", "layers", layer, "components.Z"))

def read_layer_features(directory, layer):
    return read_linerecords(os.path.join(
        directory, "steps", "pcb", "layers", layer, "features.Z"))


if __name__ == "__main__":
    #Parse commandline arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="The ODB++ directory")
    args = parser.parse_args()
    #Perform check
    print(read_layers(args.directory))
