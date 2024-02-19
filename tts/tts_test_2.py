##############################
# Ian Bernstein
# February 19th, 2024
#
# pip3 install tts
# pip3 install playsound
#
##############################

from TTS.api import TTS
from playsound import playsound

print("Hello World")

tts = TTS(model_name="tts_models/en/jenny/jenny")

tts.tts_to_file(text="... Hello, I am hacker bot...")

filename = "output.wav"

# for playing note.wav file
playsound(filename)
