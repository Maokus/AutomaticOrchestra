
import dawdreamer as daw


SAMPLE_RATE = 44100
BUFFER_SIZE = 128
PPQN = 960

engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)
engine.set_bpm(120.)  # default is 120 beats per minute.

SYNTH_PLUGIN = "/Library/Audio/Plug-Ins/VST3/BBC Symphony Orchestra.vst3"

synth = engine.make_plugin_processor("my_synth", SYNTH_PLUGIN)
assert synth.get_name() == "my_synth"

synth.open_editor()  # Open the editor, make changes, and close
name = input("enter state name")
synth.save_state("Dawdreamer/orchestra/"+name)
