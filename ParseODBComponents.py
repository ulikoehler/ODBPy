#!/usr/bin/env python3
import argparse
from ODBPy.Components import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    args = parser.parse_args()
    # Your code goes here!

    bot_components = read_linerecords(os.path.join(args.directory, "steps/pcb/layers/comp_+_bot/components.Z"))
    print(bot_components)
    components = read_components(args.directory)
    print(components)