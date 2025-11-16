"""
Functional refactor of the string normalization homework.

Goals:
- Pure functions (no prints or global state)
- Small, composable units
- Type hints + docstrings
- A single entry point `process_homework(text)`
"""

from __future__ import annotations
import re
from typing import List, Tuple

def count_whitespace(text: str) -> int:
    """Count *all* Unicode whitespace characters in text."""
    return sum(1 for ch in text if ch.isspace())

def fix_iz(text: str) -> str:
    """
    Replace mis-spelled standalone word 'iz' (any case) with 'is',
    but keep quoted “iZ” / "iZ" intact.
    """
    pattern = r'(?<![“”"])\b(?i:iz)\b(?![“”"])'
    return re.sub(pattern, 'is', text)

def split_sentences(text: str) -> List[str]:
    """
    Split text into a list alternating [chunk, delimiter, chunk, delimiter,...]
    where delimiter includes punctuation and trailing spaces.
    """
    return re.split(r'([.!?:]\s*)', text)

def sentence_case(segment: str) -> str:
    """Lowercase the segment then capitalize the first *letter* (skip leading spaces)."""
    lower = segment.lower()
    m = re.search(r'[a-zA-Z]', lower)
    if not m:
        return lower
    i = m.start()
    return lower[:i] + lower[i].upper() + lower[i+1:]

def normalize_case(text: str) -> str:
    """Apply sentence case to every sentence-like segment while preserving delimiters."""
    parts = split_sentences(text)
    out: List[str] = []
    for i, p in enumerate(parts):
        if i % 2 == 0:      # segment
            out.append(sentence_case(p))
        else:               # delimiter
            out.append(p)
    return ''.join(out)

def last_words(text: str) -> List[str]:
    """Collect the last alphabetical word of each sentence-like segment."""
    parts = split_sentences(text)
    words: List[str] = []
    for i, p in enumerate(parts):
        if i % 2 == 0:  # segment only
            tokens = re.findall(r'\b([A-Za-z]+)\b', p)
            if tokens:
                words.append(tokens[-1])
    return words

def make_sentence_from_last_words(words: List[str]) -> str:
    """Create a sentence from words and capitalize the first letter."""
    if not words:
        return ""
    s = ' '.join(words) + '.'
    return s[0].upper() + s[1:]

def process_homework(text: str) -> Tuple[str, int, str]:
    """
    Full pipeline:
    1) Count whitespace
    2) Fix 'iz' where appropriate
    3) Normalize sentence case
    4) Build and append last-words sentence

    Returns:
        final_text, whitespace_count, last_words_sentence
    """
    whitespace_count = count_whitespace(text)
    fixed = fix_iz(text)
    normalized = normalize_case(fixed)
    lw = last_words(normalized)
    extra = make_sentence_from_last_words(lw)
    final = normalized + ("\n\n" + extra if extra else "")
    return final, whitespace_count, extra


if __name__ == "__main__":
    # Example runner (I/O boundary kept here only)
    RAW = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""
    final_text, ws_count, extra = process_homework(RAW)
    print("Whitespace count:", ws_count)
    print("\n--- Final text ---\n")
    print(final_text)
