#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import multiprocessing

inf = 100
similar_chars = {u"1:2", u"2:3", u"3:4", u"4:5", u"5:6", u"6:7", u"7:8", u"8:9", u"9:0",
                 u"q:w", u"w:e", u"e:r", u"r:t", u"t:y", u"y:u", u"u:i", u"i:o", u"o:p",
                 u"a:s", u"s:d", u"d:f", u"f:g", u"g:h", u"h:j", u"j:k", u"k:l",
                 u"z:x", u"x:c", u"c:v", u"v:b", u"b:n", u"n:m",
                 u"q:a", u"a:z", u"w:s", u"s:x", u"e:d", u"d:c", u"r:f", u"f:v", u"t:g", u"g:b", u"y:h", u"h:n", u"u:j", u"j:m", u"i:k", u"o:l",
                 u"w:a", u"e:s", u"s:z", u"r:d", u"d:x", u"t:f", u"f:c", u"y:g", u"g:v", u"u:h", u"h:b", u"i:j", u"j:n", u"o:k", u"k:m", u"p:l",
                 u"e:ę", u"u:ó", u"o:ó", u"a:ą", u"l:ł", u"z:ż", u"z:ź", u"ż:ź", u"c:ć", u"n:ń",
                 u"sz:rz", u"ż:rz", u"h:ch", u"z:rz", u"ą:on", u"ę:en"}


def char_distance(a, b):
    if a == b:
        return 0
    if len(a) == 2 and len(b) == 2 and a[0] == b[1] and b[0] == a[1]:
        return 0.5
    if (a + u":" + b in similar_chars) or (b + u":" + a in similar_chars):
        return 0.5
    if len(a) == 1 and len(b) == 1:
        return 1
    return 2


def lev(word1, word2):
    if min(len(word1), len(word2)) == 0:
        return max(len(word1), len(word2))
    row = ([range(len(word1)+1), [0] * (len(word1)+1), [0] * (len(word1)+1)])
    for i in range(1, len(word2)+1):
        i0 = i % 3
        i1 = (i-1) % 3
        i2 = (i-2) % 3
        row[i0][0] = i
        for j in range(1, len(word1)+1):
            j0 = j
            j1 = j-1
            j2 = j-2
            row[i0][j0] = min(
                row[i0][j1] + 1,
                row[i1][j0] + 1,
                row[i1][j1] + char_distance(word1[j-1], word2[i-1]),
                (row[i1][j2] + char_distance(word1[j-2:j],  word2[i-1])) if j in range(2, len(word1)+1) else inf,
                (row[i2][j1] + char_distance(word1[j-1],  word2[i-2:i])) if i in range(2, len(word2)+1) else inf,
                (row[i2][j2] + char_distance(word1[j-2:j],  word2[i-2:i])) if (i in range(2, len(word2)+1)) and (j in range(2, len(word1)+1)) else inf
                )
    return row[len(word2) % 3][-1]


def distance(input):
    (word, arg) = input
    word_unicode = unicode(word[:-1], "utf-8")
    return lev(word_unicode, arg), word.decode("utf-8")

pool = multiprocessing.Pool()
parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='This script corrects misspelled words')
parser.add_argument(
    '-w', '--word',
    action='store',
    help='input word',
    dest='word')
[args, pass_args] = parser.parse_known_args()

# check all words
arg = unicode(args.word, "utf-8")
best = inf
best_val = arg
with open("data/formy_utf.txt") as file:
    words = file.readlines()
    words = zip(words, [arg]*len(words))
    words = pool.map(distance, words)
words.sort(key=lambda tup: tup[0])

# print results
for (val, word) in words[:10]:
    print(val)
    print(word)
