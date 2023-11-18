from __future__ import annotations

import io
from dataclasses import dataclass
from pydub import AudioSegment
import main
from blacksheep import Application, FromFiles

import uuid

app = Application()
post = app.router.post


@dataclass
class Response:
    transcript: str
    filler_index: list[int]
    filler_count: int
    wpm: float


@post("/api")
def home(input: FromFiles) -> Response:
    value = input.value[0]
    binary_data = value.data

    audio = AudioSegment.from_file(file=io.BytesIO(binary_data))
    output_file = f"output-{(uuid.uuid4().bytes[:8]).decode()}.wav"
    audio.export(output_file, format="wav")

    txt = main.speech_to_text(output_file)
    filler_inds = main.get_fillers(txt)
    return Response(txt, filler_inds, len(filler_inds), main.get_wpm(txt, output_file))
