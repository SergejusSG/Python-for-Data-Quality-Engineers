import re  # 1) We'll need regular expressions for precise find/replace and splitting.

# 2) Put the original text EXACTLY as given (including newlines and special quotes).
raw = """homEwork:
  tHis iz your homeWork, copy these Text to variable.



  You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.



  it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE.



  last iz TO calculate nuMber OF Whitespace characteRS in this Tex. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
"""

# 3) Count ALL whitespace characters (spaces, tabs, newlines, non-breaking spaces, etc.).
#    str.isspace() returns True for ANY Unicode whitespace character.
original_whitespace_count = sum(1 for ch in raw if ch.isspace())

# 4) Fix the misspelling: replace the WORD "iz" → "is" (any case),
#    BUT do NOT change the quoted “iZ”. We exclude matches that touch quotes.
#    - \b … \b  = match whole word
#    - (?i:iz)  = case-insensitive "iz"
#    - (?<![“”"]) and (?![“”"]) = not immediately next to “ ” or " on either side
fixed_iz = re.sub(r'(?<![“”"])\b(?i:iz)\b(?![“”"])', 'is', raw)

# 5) We need to "normalize from letter cases point of view".
#    We’ll convert text to *sentence case*: first letter uppercase, the rest lowercase for each sentence.
#    First, split the text into sentence parts, keeping the delimiters so we can put them back.
parts = re.split(r'([.!?:]\s*)', fixed_iz)

# 6) Helper to apply sentence case to a chunk WITHOUT destroying leading whitespace.
def sentence_case(segment: str) -> str:
    lower = segment.lower()            # 6a) Start by lowercasing the entire piece
    m = re.search(r'[a-zA-Z]', lower)  # 6b) Find the first letter (skip any initial spaces/newlines)
    if not m:
        return lower                   # 6c) If there’s no letter, just return as is
    i = m.start()
    # 6d) Uppercase the first letter; keep everything else lower
    return lower[:i] + lower[i].upper() + lower[i+1:]

# 7) Rebuild the normalized text while also collecting the LAST word of each sentence.
cased_parts = []
last_words = []

for i, p in enumerate(parts):
    if i % 2 == 0:  # text chunk (not the delimiter)
        seg = sentence_case(p)
        cased_parts.append(seg)
        # 7a) Grab the last alphabetical word from this chunk (if any) for the final "last-words sentence".
        words = re.findall(r'\b([A-Za-z]+)\b', seg)
        if words:
            last_words.append(words[-1])
    else:
        cased_parts.append(p)  # keep punctuation + following spaces

normalized_text = ''.join(cased_parts)

# 8) Build the extra sentence from the last words we collected.
extra_sentence = ' '.join(last_words) + '.'
#    Make sure it starts with a capital letter:
extra_sentence = extra_sentence[0].upper() + extra_sentence[1:]

# 9) Append that extra sentence to the end (as a separate paragraph).
final_text = normalized_text + "\n\n" + extra_sentence

# 10) Print results (or return them from a function in real code).
print("Original whitespace count:", original_whitespace_count)
print()
print("=== Final normalized text ===")
print(final_text)
