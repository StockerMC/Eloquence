from __future__ import annotations

# Load model directly
from pydub import AudioSegment
from transformers import pipeline
from collections import Counter
import re
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pipe = pipeline(model="distil-whisper/distil-large-v2", device=device)

filler_words = ['uh', 'uhm', 'um', 'huh', 'ah', 'er']
filler_phrases = ['like,', 'right,', ', right', 'so yeah,']

def speech_to_text(file: str) -> str:
    return pipe(file)['text']  # type: ignore


def get_words(text: str) -> list[str]:
    text = re.sub(r'[.,!?]', '', text.strip())
    return text.split()


def most_common_words(text: str) -> list[tuple[str, int]]:
    word_freq = Counter(get_words(text))
    common_words = word_freq.most_common(5)
    return common_words

def get_fillers(text: str) -> list[tuple[int, int]]:
    words = get_words(text)
    result = [(m.start(), len(substring)) for substring in (filler_words + filler_phrases) for m in re.finditer(substring, text)]
    # result = [i for i, word in enumerate(words) if word.lower() in filler_words]
    # for phrase in filler_phrases:
    #     # result.extend([case_insensitive_index(words, m.group().split()[0], m.start()) for m in re.finditer(phrase.lower(), text.lower())])
    #     words with 

    #     for m in re.finditer(phrase.lower(), text.lower()):
    #         breakpoint()
    #         result.append(case_insensitive_index(text, m.group().split()[0], m.start()))

    return result


def get_wpm(text: str, file: str) -> int:
    audio = AudioSegment.from_file(file)
    return len(get_words(text)) / (audio.duration_seconds / 60.0)

