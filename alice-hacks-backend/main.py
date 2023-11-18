# Load model directly
from transformers import pipeline
from collections import Counter
import re

pipe = pipeline(model="distil-whisper/distil-large-v2")

fillers = ['uh', 'uhm', 'um', 'huh']

def speech_to_text(file: str):
    return pipe(file)

def count_words(text: str):
    # count the most common words in text
    text = re.sub(r'.!\?', '', text.strip())
    word_freq = Counter(map(lambda s: s.lower(), text.split()))
    common_words = word_freq.most_common(5)
    return common_words


ret = speech_to_text("test.mp3")
print(ret)
print(count_words(ret['text']))


while True:
    breakpoint()