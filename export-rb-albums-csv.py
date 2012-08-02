#!/usr/bin/env python

import os
import sys

# first run the following
#egrep -A1 "<artist>.+</artist>"  ~/.local/share/rhythmbox/rhythmdb.xml| grep -v "<artist>Unknown</ar" | sed 's:<.*>\(.*\)</.*>:\1:g' > artist-albums"""

f = open('artist-albums', 'r')
out = open('artist-albums.csv', 'w')

artist = None
album = None
next = 'artist'
for line in f:
    if next == 'artist':
        artist = line.strip()
        next = 'album'
    elif next == 'album':
        album = line.strip()
        next = 'sep'
    elif next == 'sep':
        out.write('"' + artist + '","' + album + '"\n')
        next = 'artist'

out.close()
