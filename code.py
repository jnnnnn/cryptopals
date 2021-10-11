from dataclasses import dataclass
import codecs
import itertools
import collections
import pprint


def jhex(bytes: bytes):
    return codecs.encode(bytes, 'hex')


def unhex(s: str):
    return codecs.decode(s, 'hex')


def xor(v1: bytes, v2: bytes):
    if len(v1) > len(v2):
        v1, v2 = v2, v1
    return bytes([x ^ y for x, y in zip(itertools.cycle(v1), v2)])


englishfreqs = {'A': 0.082, 'B': 0.015, 'C': 0.028, 'D': 0.043, 'E': 0.13, 'F': 0.022, 'G': 0.02, 'H': 0.061, 'I': 0.07, 'J': 0.0015, 'K': 0.0077, 'L': 0.04, 'M': 0.024,
                'N': 0.067, 'O': 0.075, 'P': 0.019, 'Q': 0.00095, 'R': 0.06, 'S': 0.063, 'T': 0.091, 'U': 0.028, 'V': 0.0098, 'W': 0.024, 'X': 0.0015, 'Y': 0.02, 'Z': 0.00074, }


def freqscore(s, freqs):
    score = 0
    letters = codecs.decode(s, encoding='utf-8', errors='replace')
    counts = collections.defaultdict(int)
    for letter in letters.upper():
        counts[letter] += 1
    for letter in freqs:
        score += (freqs[letter] - counts[letter] / len(letters)) ** 2
    return score


ctext = unhex(
    '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')


@dataclass
class Candidate:
    msg: str
    key: int
    score: float


candidates = [Candidate(score=0, key=key, msg=xor(ctext, bytes([key])))
              for key in range(256)]
for c in candidates:
    c.score = freqscore(c.msg, englishfreqs)
best = sorted([c for c in candidates],
              key=lambda c: c.score)[:10]
pprint.pprint(best)
