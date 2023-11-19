from __future__ import annotations

import re
from collections import Counter
import language_tool_python
from env import OPENAI_API_KEY
from openai import OpenAI
from pydub import AudioSegment
from transformers import Pipeline

pipe: Pipeline

filler_words = ['uh', 'uhm', 'um', 'huh', 'ah', 'er']
filler_phrases = ['like,', 'right,', ', right', 'so yeah,']
tool = language_tool_python.LanguageTool('en-US')
client = OpenAI(api_key=OPENAI_API_KEY)


def speech_to_text(file: str) -> str:
    return pipe(file)['text'].strip()  # type: ignore


def get_words(text: str) -> list[str]:
    text = re.sub(r'[.,!?]', '', text.strip())
    return text.split()


def most_common_words(text: str) -> list[tuple[str, int]]:
    word_freq = Counter(get_words(text))
    common_words = word_freq.most_common(5)
    return common_words


# TODO: does not work
def get_fillers(text: str) -> list[tuple[int, int]]:
    result = [(m.start(), len(substring)) for substring in (filler_words + filler_phrases) for m in
              re.finditer(fr'(\b{substring})|({substring}\b)|(\b{substring}\b)', text, re.IGNORECASE)]
    return result


def get_total_duration(file: str) -> float:
    audio = AudioSegment.from_file(file)
    return audio.duration_seconds


def get_wpm(text: str, file: str) -> float:
    return len(get_words(text)) / (get_total_duration(file) / 60.0)


def get_grammar_mistakes(text: str) -> int:
    matches = tool.check(text)
    return len(matches)


def get_sentence_length(text: str) -> list[int]:
    sentences = re.split(r'[.!?]+', text)
    return [len(get_words(sentence)) for sentence in sentences]


def get_max_combo(filler_indices, word_count: int) -> int:
    filler_indices = [(0, 0)] + filler_indices + [(word_count, 0)]
    max_combo = max([filler_indices[i][0] - filler_indices[i - 1][0] for i in range(1, len(filler_indices))])
    return max_combo


# TODO: make harsher
def get_score(filler_count: int, wpm: float, sentence_length: list[int]) -> float:
    ans = (1 - (5 * filler_count / wpm)) * (1 - (abs(10 - sum(sentence_length) / len(sentence_length)) / 10))
    if wpm > 160:
        ans -= wpm - 160
    elif wpm < 110:
        ans -= 110 - wpm
    return max(ans, 0)


# TODO: ask user if it's a presentation, speech, etc. and for their time limit (e.g. what can they cut down on to fit the time limit)
# TODO: also ask for the tone/setting
# TODO: any other additional information they think is helpful to convey for better feedback

system_prompt = """Give me constructive criticism for my following speech. Use the following criteria:
1) Fluency (flow, avoidance of filler words/pauses, coherency)
2) Grammar (accuracy of language with grammar rules, clarity and accuracy, precision)
3) Wording (choice in vocabulary, expression richness)
4) Conciseness (efficiency in expression, direct communication, maintaining focus)
5) Logical Structure (transitions, consistency, appropriateness)

IMPORTANT: Specify each header or topic with a number and a bracket e.g. 1) Fluency.

Only comment on things very good or very bad, don't comment on things that are just okay. Be concise with feedback.
Be specific with feedback. Don't just say "good" or "bad". Give examples of what was good or bad.
Everything you say should be to help the speaker improve. Don't be mean or rude. Be encouraging and supportive.
Also, the speech length is {length} seconds long.
"""


def gpt_feedback(text: str, length: float) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt.format(
                length=round(length)
            )},
            {"role": "user", "content": f"This is the transcript: {text}"}
        ]
    )
    print(response.choices[0].message.content)
    # print(response.choices)
    # print(response.model_dump())
    return response.choices[0].message.content or 'There has been an error :('
