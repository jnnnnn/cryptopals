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

Nah, that didn't really work; the fifth-best result was

````
(1.3834, b'cOOKING\x00mc\x07S\x00LIKE\x00A\x00POUND\x00OF\x00BACON')
```. Try least-squares.
````
