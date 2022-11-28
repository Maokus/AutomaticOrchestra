#!/usr/bin/env python3

import numpy as np
from typing import List
import dawdreamer as daw
from scipy.io import wavfile


from automaticorchestra import InstrumentPathObject, render_parts, write_to_mp3

# CONSTANTS

BBCSO_PATH = "/Library/Audio/Plug-Ins/VST3/BBC Symphony Orchestra.vst3"
midi_parts_location = "AutomaticOrchestra/midi_parts/trinity/"
states_location = "AutomaticOrchestra/states/orchestra/"
SAMPLE_RATE = 44100
BUFFER_SIZE = 128
PPQN = 960  # Pulses per quarter note.

# HELPER FUNCTIONS/CLASSES

instrument_path_objects = [
    InstrumentPathObject(BBCSO_PATH, states_location +
                         "basslong", midi_parts_location+"bass.mid"),
    InstrumentPathObject(BBCSO_PATH, states_location +
                         "violong", midi_parts_location+"harmony.mid"),
    InstrumentPathObject(BBCSO_PATH, states_location +
                         "v1long", midi_parts_location+"melody.mid"),
]


audio = render_parts(instrument_path_objects, 10)

wavfile.write('AutomaticOrchestra/output.wav', SAMPLE_RATE, audio.transpose())
print(audio.ndim)
print(audio.shape)
audio = (audio/max(audio[0, :].max(), audio[1, :].max()))

write_to_mp3("AutomaticOrchestra/output.mp3",
             SAMPLE_RATE, audio.transpose(), normalized=True)
