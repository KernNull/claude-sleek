"""Pip Squeak: a tiny survey helper used to show off syntax colors."""

from __future__ import annotations

import asyncio
import re
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Optional

MAX_RETRIES = 3
EMAIL_RE = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.]+$")


@dataclass
class Answer:
    question_id: int
    text: str
    score: Optional[float] = None
    tags: list[str] = field(default_factory=list)

    def is_valid(self) -> bool:
        # A valid answer has text and a score between 0 and 1
        return bool(self.text.strip()) and (self.score is None or 0 <= self.score <= 1.0)


class Survey:
    """Collects answers and summarizes them."""

    def __init__(self, title: str, *, anonymous: bool = True) -> None:
        self.title = title
        self.anonymous = anonymous
        self._answers: dict[int, Answer] = {}

    def add(self, answer: Answer) -> None:
        if not answer.is_valid():
            raise ValueError(f"Invalid answer for question #{answer.question_id}")
        self._answers[answer.question_id] = answer

    @property
    def average(self) -> float:
        scores = [a.score for a in self._answers.values() if a.score is not None]
        return sum(scores) / len(scores) if scores else 0.0

    @staticmethod
    @lru_cache(maxsize=128)
    def is_email(value: str) -> bool:
        return EMAIL_RE.match(value) is not None


async def fetch_with_retry(url: str, retries: int = MAX_RETRIES) -> dict:
    # TODO: swap the fake delay for a real HTTP call
    for attempt in range(1, retries + 1):
        try:
            await asyncio.sleep(0.25 * attempt)
            return {"url": url, "status": 200, "ok": True}
        except asyncio.TimeoutError as exc:
            print(f"Attempt {attempt}/{retries} failed: {exc!r}")
    return {"url": url, "status": None, "ok": False}


if __name__ == "__main__":
    survey = Survey("Favorite editor theme")
    survey.add(Answer(1, "Warm and cozy", score=0.95, tags=["dark", "terracotta"]))
    survey.add(Answer(2, "Cream paper vibes", score=0.88, tags=["light"]))
    print(f"{survey.title}: average score {survey.average:.2f}")
    print(asyncio.run(fetch_with_retry("https://example.com/api")))
