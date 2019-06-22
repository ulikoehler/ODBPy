#!/usr/bin/env python3
import os.path
from collections import namedtuple
from .LineRecordParser import *
from .SurfaceParser import *
from .PolygonParser import *
from .ComponentParser import *
from .Decoder import *
from .Treeifier import *
from .Units import *

Components = namedtuple("Components", ["top", "bottom"])

def read_components(directory):
    top_components = read_linerecords(os.path.join(directory, "steps/pcb/layers/comp_+_top/components.Z"))
    bot_components = read_linerecords(os.path.join(directory, "steps/pcb/layers/comp_+_bot/components.Z"))
    return Components(parse_components(top_components), parse_components(bot_components))
