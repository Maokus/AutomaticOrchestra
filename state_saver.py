#!/usr/bin/env python3

import argparse
from automaticorchestra import gui_to_state

parser = argparse.ArgumentParser(
    prog='State Saver',
    description='Saves the state of a VST to a file',
    epilog='no epilog yet')

parser.add_argument("vst")
args = parser.parse_args()

gui_to_state(args.vst)
