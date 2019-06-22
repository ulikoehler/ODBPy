#!/usr/bin/env python3
import argparse
import itertools
from collections import namedtuple
from ODBPy.Components import *
from XLSXUtils import *

ComponentInfo = namedtuple("ComponentInfo", ["Name", "Value", "MPN"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", help="ODB++ directory to read")
    parser.add_argument("-o","--outfile", default="BOM.xlsx", help="XLSX file to write")
    args = parser.parse_args()
    # Parse components (top and bot)
    components = read_components(args.directory)
    # Remap by component name
    all_components = [
        ComponentInfo(
            component.name,
            component.properties.get("Value", ""),
            component.properties.get("Name", "")
        )
        for component in itertools.chain(components.top.values(), components.bot.values())
    ]
    print(f'Found {len(all_components)} components')
    namedtuples_to_xlsx(args.outfile, all_components)

