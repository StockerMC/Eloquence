from __future__ import annotations

# Load model directly
from pydub import AudioSegment
from transformers import pipeline
from collections import Counter
import re
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pipe = pipeline(model="distil-whisper/distil-large-v2", device=device)

fillers = ['uh', 'uhm', 'um', 'huh']


def speech_to_text(file: str) -> str:
    return pipe(file)['text']  # type: ignore


def get_words(text: str) -> list[str]:
    text = re.sub(r'[.,!?]', '', text.strip())
    return text.split()


def most_common_words(text: str) -> list[tuple[str, int]]:
    word_freq = Counter(get_words(text))
    common_words = word_freq.most_common(5)
    return common_words


def get_fillers(text: str) -> list[int]:
    words = get_words(text)
    return [i for i, word in enumerate(words) if word.lower() in fillers]


def get_wpm(text: str, file: str) -> int:
    audio = AudioSegment.from_file(file)
    return len(get_words(text)) / (audio.duration_seconds / 60.0)

