#!/usr/bin/env python
'''
Demo for SAR visualizer.
'''

import os
import sys
import pprint
from sar import parser
from sar import viz

def main(in_sar_log, output_path):
	insar = parser.Parser(in_sar_log)
	sar_viz = viz.Visualization(insar.get_sar_info())
	sar_viz.save(output_path)

def set_include_path():
    include_path = os.path.abspath("./")
    sys.path.append(include_path)

if __name__ == "__main__":
	set_include_path()
	main(sys.argv[1], sys.argv[2])
