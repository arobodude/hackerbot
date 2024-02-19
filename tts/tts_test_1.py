##############################
# Ian Bernstein
# February 19th, 2024
#
# pip3 install tts
#
##############################

from TTS.api import TTS

print("Hello World")

tts = TTS(model_name="tts_models/en/jenny/jenny")

tts.tts_to_file(text="Hello, I am hacker bot.")
