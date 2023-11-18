#TESTING
from transformers import pipeline
from datetime import datetime

pipe = pipeline(task="automatic-speech-recognition", model="distil-whisper/distil-large-v2")

print(pipe("test.mp3"))