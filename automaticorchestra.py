import pydub
import numpy as np
from typing import List
import dawdreamer as daw

import random
import string

SAMPLE_RATE = 44100
BUFFER_SIZE = 128
PPQN = 960  # Pulses per quarter note.

# CLASSES


class InstrumentPathObject:
    def __init__(self, vst_path, state_path, midi_path):
        self.vst_path = vst_path
        self.state_path = state_path
        self.midi_path = midi_path

# AUDIO DATA HANDLING


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


def normalise(audio):
    # Where audio is a numpy array
    return (audio/max(audio[0, :].max(), audio[1, :].max()))

# RENDERING


def make_output_funnel(engine):
    # Convert an instrument of up to 16 stereo outputs to 1 stereo output
    funnel = engine.make_add_processor(
        # Unique string identifier
        "output_funnel_"+''.join(random.choices(string.ascii_lowercase, k=5)),
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    )
    print(funnel.get_num_input_channels())
    return funnel


def render_parts(ipos: List[InstrumentPathObject], duration):
    # IPOs: InstrumentPathObjects

    engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
    engine.set_bpm(60.)

    synthesizers = []
    funneled_synths = []
    graph = []

    # Load synths
    for i in range(len(ipos)):
        synth_label = "synthesizer_"+str(i)
        current_synth = engine.make_plugin_processor(
            synth_label, ipos[i].vst_path)

        synthesizers.append(
            current_synth
        )

        assert current_synth.get_name() == synth_label

        if(ipos[i].state_path != None):
            current_synth.load_state(ipos[i].state_path)
        else:
            current_synth.open_editor()

        current_synth.load_midi(ipos[i].midi_path, beats=True)

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


def gui_to_state(vstpath):
    # Opens the GUI for the VST, and on close prompts for the name of the state.

    # Setup dawdreamer for processing
    engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
    engine.set_bpm(120.)  # default is 120 beats per minute.
    synth = engine.make_plugin_processor("my_synth", vstpath)
    assert synth.get_name() == "my_synth"

    synth.open_editor()  # Open the editor, make changes, and close
    name = input("enter state name: ")
    synth.save_state(name)
