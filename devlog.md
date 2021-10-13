# Cryptopals: Matasano Cryptography Exercises.

https://cryptopals.com

## Set 1: Qualifiers

> This is the qualifying set. We picked the exercises in it to ramp developers up gradually into coding cryptography, but also to verify that we were working with people who were ready to write code.
>
> This set is relatively easy. With one exception, most of these exercises should take only a couple minutes. But don't beat yourself up if it takes longer than that. It took Alex two weeks to get through the set!
>
> If you've written any crypto code in the past, you're going to feel like skipping a lot of this. Don't skip them. At least two of them (we won't say which) are important stepping stones to later attacks.

### Exercise 1: Convert hex to base64

Search google: `python convert hex to base64`. Find [this answer](https://stackoverflow.com/a/42230475/412529).

Write code. `python code.py`. Prints the answer. done.

### Exercise 2: XOR

Write function. I already know that python's XOR operator is `|`. Test code. Uh, I mean `^` lol. OK, it works.

### Exercise 3: XOR decrypt (single char key)

Text suggests computing letter frequency. google `english letter character frequency table`.

Wikipedia [has one](https://en.wikipedia.org/wiki/Letter_frequency).

Probably best to do least-squares difference (i.e. `(actual freq - expected freq) ^^2` for each letter, summed). But let's see if linear works because that doesn't require keeping count of all the letters, only the total sum.

Nah, that didn't really work; the fifth-best result was this.

```
(1.3834, b'cOOKING\x00mc\x07S\x00LIKE\x00A\x00POUND\x00OF\x00BACON')
```

Try least-squares. Still not great. I think the spaces in the text are screwing up the percentages. google `ascii frequency table`. https://opendata.stackexchange.com/a/7043 gives all 128 chars. OK, that table worked much better.

```
$ python code.py
[Candidate(msg=b"Cooking MC's like a pound of bacon", key=88, score=0.030906742394673607),
 Candidate(msg=b'\x9b\xb7\xb7\xb3\xb1\xb6\xbf\xf8\x95\x9b\xff\xab\xf8\xb4\xb1\xb3\xbd\xf8\xb9\xf8\xa8\xb7\xad\xb6\xbc\xf8\xb7\xbe\xf8\xba\xb9\xbb\xb7\xb6', key=128, score=0.06350430711846337),
 Candidate(msg=b'\x9a\xb6\xb6\xb2\xb0\xb7\xbe\xf9\x94\x9a\xfe\xaa\xf9\xb5\xb0\xb2\xbc\xf9\xb8\xf9\xa9\xb6\xac\xb7\xbd\xf9\xb6\xbf\xf9\xbb\xb8\xba\xb6\xb7', key=129, score=0.06350430711846337),
```

> Achievement Unlocked
>
> You now have our permission to make "ETAOIN SHRDLU" jokes on Twitter.

what? oh. [wiki](https://en.wikipedia.org/wiki/Etaoin_shrdlu)

> It is the approximate order of frequency of the 12 most commonly used letters in the English language.

## Exercise 4: 300 single-char xors

Code it. worked first try. Took a few seconds to run lol. My python is slow.

## Exercise 5: Implement repeating-key XOR

Lol, defensive programming; I already did the repeating the shorter string because `zip()` stops early otherwise.

Done. I used to use a firewall called BlackIce. Lmao. That was before Windows had a firewall and also before NAT.

## Exercise 6: Break repeating-key XOR

> It is officially on, now.
>
> Breaking repeating-key XOR ("Vigenere") statistically is obviously an academic exercise, a "Crypto 101" thing. But more people "know how" to break it than can actually break it, and a similar technique breaks something much more important.

I'm excited.

Computing hamming distance between two byte arrays. Google for `bit difference python`. nothing helpful. google `count number of different bits python`. ah, [perfect](https://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-positive-integer). The `bin()` function returns the bit representation as a string, then strings have a `count` function that we can use to count the 1s. If we xor the two arrays together, then every time there's a difference the Xor result will have a `1` at that position.

implementing the repeating key part.

load base64 file. google `python load base64 file`. [result](https://www.kite.com/python/examples/3422/base64-decode-a-%60base64%60-file). copy/paste lmao.

ok, best key guess is 5. but that didn't work. Meh. try every keysize. ah, there's one:

    Best key guess is b'Terminator X: Bring the noise'

done.

## Exercise 7: AES

Ugh, aes in python is a pain. What's the library these days? google `python aes library`. Choices seem to include:
1. Pycryptodome (first google link)
2. Cryptography (recommended by [stackoverflow](https://stackoverflow.com/questions/25261647/python-aes-encryption-without-extra-module))
3. Pycrypto (official docs used to recommend)

I'm going to go with stackoverflow's recommendation. Create requirements.txt.

    py -m pip install -r requirements.txt

> I like "YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do too

OK, need to decrypt AES. check [library docs](https://cryptography.io/en/latest/) for example code. Oh, bugger. It doesn't support ECB, only CBC. ok, uninstall. google `python aes ecb`. stackoverflow has [a good example](https://stackoverflow.com/questions/67265485/python-aes-ecb-mode-with-crypto). What is the package called? google `python aes`. pycryptodome [example](https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html) is the same as the stackoverflow answer. ok. installation [says](https://pycryptodome.readthedocs.io/en/latest/src/installation.html) `pip install pycryptodome`. cool. Get error.

    TypeError: object of type 'EcbMode' has no len()

derp, called `cipher` and `ciphertext` the same variable name. fixed. working.

## Exercise 8: AES ECB detection

> Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext block will always produce the same 16 byte ciphertext.

I don't quite understand this. Am I supposed to know what the first 16 bytes of the plaintext is? The last few cyphertexts have always been the same... the first few bytes are `I'm back and I'm ringin' the bell\nA rockin' on the mike while the fly girls yell`

The first bytes of ex7 cyphertext encoded as hex are `091230aade3eb330`. That doesn't appear in the ex8 file.

Maybe the plaintext block is all nulls? Encrypt 16 bytes of 0 with a couple of different keys. No matches.

Google `detect aes ecb`. Lots of cryptopals solutions :(. In particular, [this one](https://stackoverflow.com/a/20723807/412529):

> with the assumption that some repeated plaintext blocks occur at the same ciphertext block offsets, we can simply go ahead and look for repeated ciphertext blocks of various lengths. 

Oh, I get it now. ECB doesn't depend on previous blocks, there's no chaining. So each 16-byte block may as well have been encrypted on its own. So there might be repeated blocks. 

OK, so search for repeats. ah.

    line 132 repeated at 16, 1 times

let's try decoding it with the key from the previous exercise. no luck. I guess it's a mystery.

## Set 2: Block ciphers 1

### Exercise 9: Implement PKCS#7 padding

