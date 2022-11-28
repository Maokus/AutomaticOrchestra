#!/usr/bin/env python3


import argparse
from automaticorchestra import InstrumentPathObject, normalise, render_parts, write_to_mp3, SAMPLE_RATE

# SETUP

parser = argparse.ArgumentParser(
    prog='Automatic Orchestra',
    description='Renders MIDI file into an MP3 or WAV',
    epilog='no epilog yet')

parser.add_argument("vst")
parser.add_argument("midi")
parser.add_argument("output")
parser.add_argument("-s", "--state")
parser.add_argument("-l", "--audiolength", default=10)

args = parser.parse_args()


instrument_path_objects = [
    InstrumentPathObject(args.vst, args.state, args.midi)
]

audio = normalise(render_parts(instrument_path_objects, args.audiolength))

write_to_mp3(args.output,
             SAMPLE_RATE, audio.transpose(), normalized=True)
