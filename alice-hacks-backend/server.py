from __future__ import annotations

import io
import os
import uuid
from dataclasses import dataclass
import torch
import util
from blacksheep import Application, FromFiles
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
    grammar_mistakes: int

@post("/test")
def test(input: FromFiles) -> Response:
    return Response(transcript=r"""Um, what do I begin? Let's start with this. Uh, I'm sorry. Um, this is a first for me. I've never faced criticism like this before. Uh, so yeah, I'm surrounded by 
good people, and, um, I believe I make good decisions, but I'm still a human being, so, uh, so yeah, I'm surrounded by good people, and, um, I believe I make good decisions, but I'm st
ill a human being, so, uh, I can't, I can be wrong.""", filler_indices=[], filler_count=0, wpm=167.4359457422758, words=['Um', 'what', 'do', 'I', 'begin', "Let's", 'start', 'with', 'this', 'Uh', r"I'm", 'sorry', 'Um', 'this', 'is', 'a', 'first', 'for', 'me', r"I've", 'never', 'faced', 'criticism', 'like', 'this', 'before', 'Uh', 'so', 'yeah', "I'm", 'surrounded', 'by',
'good', 'people', 'and', 'um', 'I', 'believe', 'I', 'make', 'good', 'decisions', 'but', "I'm", 'still', 'a', 'human', 'being', 'so', 'uh', 'so', 'yeah', "I'm", 'surrounded', 'by', 'good', 'people', 'and', 'um', 'I', 'believe', 'I', 'make', 'good', 'decisions', 'but', "I'm", 'still', 'a', 'human', 'being', 'so', 'uh', 'I', "can't", 'I', 'can', 'be', 'wrong'], sentence_length=[5, 4, 3, 7, 7, 53, 0], overall_score=0.8714285714285713, most_common_words=[('I', 7), ("I'm", 5), ('so', 4), ('good', 4), ('this', 3)], detailed_feedback=r"""1) Fluency:\n- Ther
e are multiple instances of filler words and pauses throughout the speech (e.g., "um," "uh," "so yeah"). It disrupts the flow and makes the speech sound less confident.\n- The repetiti
on of the phrase "so yeah, I\'m surrounded by good people, and, um, I believe I make good decisions" feels redundant and lacks coherence.\n- The sentence "I can\'t, I can be wrong" is 
not structured smoothly and may cause confusion for the listener.\n\n2) Grammar:\n- The sentence "I can\'t, I can be wrong" lacks clarity and accuracy. It needs to be rephrased for cor
rect and precise meaning.\n\n5) Logical Structure:\n- The speech lacks a clear structure or logical flow. It jumps between different ideas without smooth transitions, causing some conf
usion for the listener.\n\nOverall, the speaker should work on reducing filler words and pauses, organizing their thoughts more coherently, and improving the clarity and grammar of their sentences for better overall fluency and logical structure.""",
                    duration=28.309333333333335,
                    grammar_mistakes=0)


@post("/api")
def home(input: FromFiles) -> Response:
    print('hello')
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
        grammar_mistakes=get_grammar_mistakes(text),
    )

    print(res)
    os.remove(output_file)

    return res
