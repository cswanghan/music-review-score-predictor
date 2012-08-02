#!/usr/bin/env python
from bs4 import BeautifulSoup
import csv
from lxml import html
import os
import sys

if len(sys.argv) < 2:
    print "Usage"
    sys.exit(1)

genre = sys.argv[1]

datadir = 'mc-data/' + genre

csvfile = open(os.path.join(datadir, genre + '.csv'), 'w')
writer = csv.writer(csvfile)
writer.writerow(['Artist', 'Album', 'Score'])
for page in sorted(os.listdir(datadir)):
    if page.endswith('html'):
        print 'parsing page ' + page
        page_file = open(os.path.join(datadir, page), 'r')
        doc = html.parse(page_file).getroot()
        try:
            for li in doc.cssselect('li.release_product'):
                album = li.cssselect('div.product_title')[0].text_content().strip()
                score = li.cssselect('span.metascore')[0].text_content().strip()
                artist = li.cssselect('li.product_artist')[0].cssselect('span.data')[0].text_content().strip()
                print 'artist: %s, album: %s, score: %s' % (artist, album, score)
                writer.writerow([artist, album, score])

        except Exception as e:
            print e

csvfile.close()