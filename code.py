from dataclasses import dataclass
import codecs
import itertools
import collections


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

asciicharfreqs = collections.defaultdict(float, {32: 0.167564443682168, 101: 0.08610229517681191, 116: 0.0632964962389326, 97: 0.0612553996079051, 110: 0.05503703643138501, 105: 0.05480626188138746, 111: 0.0541904405334676, 115: 0.0518864979648296, 114: 0.051525029341199825, 108: 0.03218192615049607, 100: 0.03188948073064199, 104: 0.02619237267611581, 99: 0.02500268898936656, 10: 0.019578060965172565, 117: 0.019247776378510318, 109: 0.018140172626462205, 112: 0.017362092874808832, 102: 0.015750347191785568, 103: 0.012804659959943725, 46: 0.011055184780313847, 121: 0.010893686962847832, 98: 0.01034644514338097, 119: 0.009565830104169261, 44: 0.008634492219614468, 118: 0.007819143740853554, 48: 0.005918945715880591, 107: 0.004945712204424292, 49: 0.004937789430804492, 83: 0.0030896915651553373, 84: 0.0030701064687671904, 67: 0.002987392712176473, 50: 0.002756237869045172, 56: 0.002552781042488694, 53: 0.0025269211093936652, 65: 0.0024774830020061096, 57: 0.002442242504945237, 120: 0.0023064144740073764, 51: 0.0021865587546870337, 73: 0.0020910417959267183, 45: 0.002076717421222119, 54: 0.0019199098857390264, 52: 0.0018385271551164353, 55: 0.0018243295447897528, 77: 0.0018134911904778657, 66: 0.0017387002075069484, 34: 0.0015754276887500987, 39: 0.0015078622753204398, 80: 0.00138908405321239,
                                                 69: 0.0012938206232079082, 78: 0.0012758834637326799, 70: 0.001220297284016159, 82: 0.0011037374385216535, 68: 0.0010927723198318497, 85: 0.0010426370083657518, 113: 0.00100853739070613, 76: 0.0010044809306127922, 71: 0.0009310209736100016, 74: 0.0008814561018445294, 72: 0.0008752446473266058, 79: 0.0008210528757671701, 87: 0.0008048270353938186, 106: 0.000617596049210692, 122: 0.0005762708620098124, 47: 0.000519607185080999, 60: 0.00044107665296153596, 62: 0.0004404428310719519, 75: 0.0003808001912620934, 41: 0.0003314254660634964, 40: 0.0003307916441739124, 86: 0.0002556203680692448, 89: 0.00025194420110965734, 58: 0.00012036277683200988, 81: 0.00010001709417636208, 90: 8.619977698342993e-05, 88: 6.572732994986532e-05, 59: 7.41571610813331e-06, 63: 4.626899793963519e-06, 127: 3.1057272589618137e-06, 94: 2.2183766135441526e-06, 38: 2.0282300466689395e-06, 43: 1.5211725350017046e-06, 91: 6.97204078542448e-07, 93: 6.338218895840436e-07, 36: 5.070575116672349e-07, 33: 5.070575116672349e-07, 42: 4.436753227088305e-07, 61: 2.5352875583361743e-07, 126: 1.9014656687521307e-07, 95: 1.2676437791680872e-07, 9: 1.2676437791680872e-07, 123: 6.338218895840436e-08, 64: 6.338218895840436e-08, 5: 6.338218895840436e-08, 27: 6.338218895840436e-08, 30: 6.338218895840436e-08})


def freqscore(s, freqs=asciicharfreqs):
    score = 0
    chars = codecs.decode(s, encoding='utf-8', errors='replace')
    counts = collections.defaultdict(int)
    for char in chars:
        counts[char] += 1
    for char in freqs:
        score += (freqs[char] - (counts[chr(char)] / len(chars))) ** 2
    return score


def bestxor(s: bytes):
    @dataclass
    class Candidate:
        msg: str
        key: int
        score: float

    candidates = [Candidate(score=0, key=key, msg=xor(s, bytes([key])))
                  for key in range(256)]
    for c in candidates:
        c.score = freqscore(c.msg)
    candidates.sort(key=lambda c: c.score)
    return candidates[0]


def hammingdist(b1s: bytes, b2s: bytes):
    return sum(bin(n).count("1") for n in xor(b1s, b2s))


def crackXorRepeat(cipher: bytes):
    nh, keysize = 1e10, 1
    for ks in range(2, min(40, len(cipher)//4)):
        block1 = cipher[0:ks]
        block2 = cipher[ks:ks*2]
        nicer = hammingdist(block1, block2) / ks
        if nicer < nh:
            nh, keysize = nicer, ks
    print(f"Best keysize is {keysize}")

    for keysize in range(2, 40):
        key = b''
        for keyindex in range(keysize):
            partcipher = b"".join([cipher[i:i+1]
                                   for i in range(keyindex, len(cipher), keysize)])
            bestguess = bestxor(partcipher)
            key += bytes([bestguess.key])
        print(f"Best key guess is {key}")


def loadbase64file(fname: str):
    import base64
    with open(fname, "r") as f:
        return base64.b64decode(f.read())


cipher = loadbase64file('data-ex6.txt')
print(xor(cipher, b'Terminator X: Bring the noise').decode(
    'utf-8', errors='replace'))
