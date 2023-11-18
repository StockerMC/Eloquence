from __future__ import annotations

import re
from collections import Counter

import torch
from env import OPENAI_API_KEY
from openai import OpenAI
from pydub import AudioSegment
from transformers import pipeline

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

pipe = pipeline(model="distil-whisper/distil-large-v2", device=device)

filler_words = ['uh', 'uhm', 'um', 'huh', 'ah', 'er']
filler_phrases = ['like,', 'right,', ', right', 'so yeah,']

client = OpenAI(api_key=OPENAI_API_KEY)
system_prompt = ""


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
    result = [(m.start(), len(substring)) for substring in (filler_words + filler_phrases) for m in re.finditer(substring, text)]
    return result


def get_wpm(text: str, file: str) -> int:
    audio = AudioSegment.from_file(file)
    return len(get_words(text)) / (audio.duration_seconds / 60.0)


def get_sentence_length(text: str) -> list[int]:
    sentences = re.split(r'[.!?]+', text)
    return [len(get_words(sentence)) for sentence in sentences]


def get_score(filler_count: int, wpm: int, sentence_length: list[int]) -> float:
    return (1 - (filler_count / wpm)) * (1 - (abs(10 - sum(sentence_length) / len(sentence_length)) / 10))


def gpt_feedback(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    return response
