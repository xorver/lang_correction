#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

similar_chars = {u"12", u"23", u"34", u"45", u"56", u"67", u"78", u"89", u"90",
                 u"qw", u"we", u"er", u"rt", u"ty", u"yu", u"ui", u"io", u"op",
                 u"as", u"sd", u"df", u"fg", u"gh", u"hj", u"jk", u"kl",
                 u"zx", u"xc", u"cv", u"vb", u"bn", u"nm",
                 u"qa", u"az", u"ws", u"sx", u"ed", u"dc", u"rf", u"fv", u"tg", u"gb", u"yh", u"hn", u"uj", u"jm", u"ik", u"ol",
                 u"wa", u"es", u"sz", u"rd", u"dx", u"tf", u"fc", u"yg", u"gv", u"uh", u"hb", u"ij", u"jn", u"ok", u"km", u"pl",
                 u"eę", u"uó", u"oó", u"aą", u"lł", u"zż", u"zź", u"żź", u"cć", u"nń"}


def char_distance(a, b):
    if a == b:
        return 0
    if (a+b in similar_chars) or (b+a in similar_chars):
        return 0.5
    return 1


def lev(word1, word2):
    if min(len(word1), len(word2)) == 0:
        return max(len(word1), len(word2))
    up_row = range(len(word1)+1)
    down_row = [0] * (len(word1)+1)
    for i in range(1, len(word2)+1):
        down_row[0] = i
        for j in range(1, len(word1)+1):

            down_row[j] = min(down_row[j-1] + 1, up_row[j] + 1, up_row[j-1] + char_distance(word1[j-1], word2[i-1]))
        up_row, down_row = down_row, up_row
    return up_row[-1]

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='This script corrects misspelled words')
parser.add_argument(
    '-w', '--word',
    action='store',
    help='input word',
    dest='word')
[args, pass_args] = parser.parse_known_args()

# standard way
best = 999
best_val = args.word
with open("data/formy_utf.txt") as file:
    for word in file:
        distance = lev(word, args.word)
        if distance < best:
            best, best_val = distance, word
            print(best_val)

print(best_val)