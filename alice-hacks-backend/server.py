from __future__ import annotations

import io
import os
import uuid
from dataclasses import dataclass

import torch
import util
from blacksheep import Application, FromFiles
from pydub import AudioSegment
from transformers import pipeline
from util import *

app = Application()
post = app.router.post

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
util.pipe = pipeline(model="distil-whisper/distil-large-v2", device=device)

@dataclass
class Response:
    transcript: str
    filler_indices: list[tuple[int, int]]
    filler_count: int
    wpm: float
    words: list[str]
    sentence_length: list[int]
    overall_score: float
    most_common_words: list[tuple[str, int]]
    detailed_feedback: str
    duration: float


@post("/api")
def home(input: FromFiles) -> Response:
    value = input.value[0]
    binary_data = value.data

    audio = AudioSegment.from_file(file=io.BytesIO(binary_data))
    output_file = f"temp/output-{(str(uuid.uuid4())[:8])}.wav"
    audio.export(output_file, format="wav")

    text = speech_to_text(output_file)
    filler_indices = get_fillers(text)
    filler_count = len(filler_indices)
    wpm = get_wpm(text, output_file)
    sentence_length = get_sentence_length(text)
    duration = get_total_duration(output_file)

    res = Response(
        transcript=text,
        filler_indices=filler_indices,
        filler_count=filler_count,
        wpm=wpm,
        words=get_words(text),
        sentence_length=get_sentence_length(text),
        overall_score=get_score(filler_count, wpm, sentence_length),
        most_common_words=most_common_words(text),
        detailed_feedback=gpt_feedback(text, duration),
        duration=duration,
    )

    print(res)
    os.remove(output_file)

    return res
