#!/usr/bin/env python3


import argparse
from automaticorchestra import InstrumentPathObject, render_parts, write_to_mp3, SAMPLE_RATE
from scipy.io import wavfile

# SETUP

parser = argparse.ArgumentParser(
    prog='Automatic Orchestra',
    description='Renders MIDI file into an MP3 or WAV',
    epilog='no epilog yet')

parser.add_argument("vst")
parser.add_argument("midi")
parser.add_argument("output")
parser.add_argument("-s", "--state")

args = parser.parse_args()

instrument_path_objects = [
    InstrumentPathObject(args.vst, args.state, args.midi)
]

audio = render_parts(instrument_path_objects, 10)

audio = (audio/max(audio[0, :].max(), audio[1, :].max()))

write_to_mp3(args.output,
             SAMPLE_RATE, audio.transpose(), normalized=True)
