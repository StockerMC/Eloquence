from __future__ import annotations

import re
from collections import Counter

from env import OPENAI_API_KEY
from openai import OpenAI
from pydub import AudioSegment
from transformers import Pipeline

pipe: Pipeline

filler_words = ['uh', 'uhm', 'um', 'huh', 'ah', 'er']
filler_phrases = ['like,', 'right,', ', right', 'so yeah,']

client = OpenAI(api_key=OPENAI_API_KEY)

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
    result = [(m.start(), len(substring)) for substring in (filler_words + filler_phrases) for m in re.finditer(f'(\b{substring})|({substring}\b)|(\b{substring}\b)', text)]
    return result


def get_wpm(text: str, file: str) -> int:
    audio = AudioSegment.from_file(file)
    return len(get_words(text)) / (audio.duration_seconds / 60.0)


def get_sentence_length(text: str) -> list[int]:
    sentences = re.split(r'[.!?]+', text)
    return [len(get_words(sentence)) for sentence in sentences]


def get_score(filler_count: int, wpm: int, sentence_length: list[int]) -> float:
    return (1 - (filler_count / wpm)) * (1 - (abs(10 - sum(sentence_length) / len(sentence_length)) / 10))


# TODO: ask user if it's a presentation, speech, etc. and for their time limit (e.g. what can they cut down on to fit the time limit)
# TODO: also ask for the tone/setting
# TODO: any other additional information they think is helpful to convey for better feedback

system_prompt = """This is for a website called Eloquence where we aim to improve people's speaking skills by acting as Grammarly for speaking. Essentially, your job is to critique transcribed text in terms of the following, which is going to be judged based on the following criteria:
1) Fluency (smoothness and flow, avoidance of filler words/pauses, coherency)
2) Grammar (accuracy of language with grammar rules, clarity and accuracy, precision)
3) Wording (thoughtful/impactful choice in vocabulary, effective arrangement, expression richness)
4) Conciseness (efficiency in expression, direct communication, maintaining focus)
5) Logical Structure (transitions, consistency, appropriateness)
6) Communication (repetition and redundancy, engagement, clarity of expression)
"""

def gpt_feedback(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"This is the transcript: {text}"}
        ]
    )
    print(response)
    print(response.choices)
    print(response.model_dump())
    return response
