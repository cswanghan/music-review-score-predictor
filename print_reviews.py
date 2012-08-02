import os
import pitchfork
import sys

data_dir = sys.argv[1]

rev = None
for root, dirs, files in os.walk(data_dir):
    for file in files:
        if file.endswith('html'):
            rev = pitchfork._parse_review_html(
                open(os.path.join(root, file), 'r'))
            print "Artist: " + rev.artist
            print "Album: " + rev.album
            print "Score: " + str(rev.score)
            print rev.text
            print ""
