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

Components = namedtuple("Components", ["top", "bot"])

def read_components(directory):
    top_path = os.path.join(directory, "steps/pcb/layers/comp_+_top/components.Z")
    top_components = read_linerecords(top_path) if os.path.isfile(top_path) else {}
    bot_path = os.path.join(directory, "steps/pcb/layers/comp_+_bot/components.Z")
    bot_components = read_linerecords(bot_path) if os.path.isfile(bot_path) else {}
    return Components(parse_components(top_components), parse_components(bot_components))
