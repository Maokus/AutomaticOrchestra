import pydub
import numpy as np
from typing import List
import dawdreamer as daw
from scipy.io import wavfile

import random
import string

# Edit this string to where you keep the BBCSO vst
BBCSO_PATH = "/Library/Audio/Plug-Ins/VST3/BBC Symphony Orchestra.vst3"

SAMPLE_RATE = 44100
BUFFER_SIZE = 128
PPQN = 960  # Pulses per quarter note.

# write_to_mp3 function by Basj at https://stackoverflow.com/a/53633178/11556921


def write_to_mp3(f, sr, x, normalized=False):
    """numpy array to MP3"""
    channels = 2 if (x.ndim == 2 and x.shape[1] == 2) else 1
    if normalized:  # normalized array - each item should be a float in [-1, 1)
        y = np.int16(x * 2 ** 15)
    else:
        y = np.int16(x)
    song = pydub.AudioSegment(
        y.tobytes(), frame_rate=sr, sample_width=2, channels=channels)
    song.export(f, format="mp3", bitrate="320k")


class InstrumentPathObject:
    def __init__(self, vst_path, state_path, midi_path):
        self.vst_path = vst_path
        self.state_path = state_path
        self.midi_path = midi_path


def make_output_funnel(engine):
    funnel = engine.make_add_processor(
        # Just some unique string
        "output_funnel_"+''.join(random.choices(string.ascii_lowercase, k=5)),
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    return funnel

# IPOs: InstrumentPathObjects


def render_parts(ipos: List[InstrumentPathObject], duration):

    engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
    engine.set_bpm(60.)

    synthesizers = []
    funneled_synths = []  # To transform 16 outputs into 1 outputs
    graph = []

    for i in range(len(ipos)):
        synth_label = "synthesizer_"+str(i)
        current_synth = engine.make_plugin_processor(
            synth_label, ipos[i].vst_path)
        synthesizers.append(
            current_synth
        )
        assert current_synth.get_name() == synth_label

        current_synth.load_state(ipos[i].state_path)
        current_synth.load_midi(ipos[i].midi_path, beats=True)

    # All synths loaded fine

    for synth in synthesizers:
        funnel = make_output_funnel(engine)
        funneled_synths.append(funnel)
        graph.append((synth, []))
        graph.append((funnel, [synth.get_name()]))

    graph.append((engine.make_add_processor("added", [1 for i in range(len(ipos))]),
                  [funnel.get_name() for funnel in funneled_synths]))

    engine.load_graph(graph)

    #Graph is loaded

    engine.render(duration)
    audio = engine.get_audio()
    return audio


midi_parts_location = "AutomaticOrchestra/midi_parts/trinity/"
states_location = "AutomaticOrchestra/orchestra/"

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
