import codecs
import itertools


def jhex(bytes: bytes):
    return codecs.encode(bytes, 'hex')


def unhex(s: str):
    return codecs.decode(s, 'hex')


def xor(v1: bytes, v2: bytes):
    if len(v1) > len(v2):
        v1, v2 = v2, v1
    return [x ^ y for x, y in zip(itertools.cycle(v1), v2)]


v1 = unhex('1c0111001f010100061a024b53535009181c')
v2 = unhex('686974207468652062756c6c277320657965')

result = xor(v1, v2)

print(jhex(bytes(result)))
