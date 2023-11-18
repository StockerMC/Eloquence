import io
from dataclasses import dataclass
from pydub import AudioSegment
import main
from blacksheep import Application, FromFiles

app = Application()
post = app.router.post


@dataclass
class Response:
    transcript: str
    filler_index: [int]
    filler_count: int
    wpm: float


@post("/api")
def home(input: FromFiles):
    value = input.value[0]
    binary_data = value.data
    print(value.content_type)
    audio = AudioSegment.from_file(file=io.BytesIO(binary_data))
    output_file = "output.wav"
    audio.export(output_file, format="wav")
    return main.speech_to_text(output_file)