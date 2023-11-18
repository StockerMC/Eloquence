from __future__ import annotations

import io
from dataclasses import dataclass
from pydub import AudioSegment
import main
from blacksheep import Application, FromFiles
import os

import uuid

app = Application()
post = app.router.post


@dataclass
class Response:
    transcript: str
    filler_indices: list[tuple[int, int]]
    filler_count: int
    wpm: float
    words: list[str]
    sentence_length: list[int]
    overall_score: float


@post("/api")
def home(input: FromFiles) -> Response:
    value = input.value[0]
    binary_data = value.data

    audio = AudioSegment.from_file(file=io.BytesIO(binary_data))
    output_file = f"temp/output-{(str(uuid.uuid4())[:8])}.wav"
    audio.export(output_file, format="wav")

    txt = main.speech_to_text(output_file)
    filler_inds = main.get_fillers(txt)
    print(f"text: {txt}")
    print(f"filler_inds: {filler_inds}")
    print(f"filler_count: {len(filler_inds)}")
    print(f"wpm: {main.get_wpm(txt, output_file)}")
    res = Response(txt, filler_inds, len(filler_inds), main.get_wpm(txt, output_file), main.get_words(txt),
                   main.get_sentence_length(txt), main.get_score(len(filler_inds), main.get_wpm(txt, output_file), main.get_sentence_length(txt)))
    os.remove(output_file)
    return res
