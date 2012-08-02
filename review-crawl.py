#!/usr/bin/env python

import sys
import os
import re
import time

if len(sys.argv) < 4:
    print "Usage: review-crawl.sh startPage endPage"
    sys.exit(1)

start = int(sys.argv[1])
end = int(sys.argv[2])

# in format 1,3,5, for sampling purposes
commasep_indexes = sys.argv[3]
str_indexes = commasep_indexes.split(',')
indexes = [int(i) for i in str_indexes]
print indexes

dry_run = False
if len(sys.argv) > 4:
   if sys.argv[4] == 'dry':
        dry_run = True
        print "dry run"

for i in range(start,end):
    data_dir = 'data/%d/' % i 
    urls = open(data_dir + 'urls', 'r').readlines()
    for idx, url in enumerate(urls):
        if idx in indexes: 
            print idx
            url = 'http://pitchfork.com' + url.rstrip()
            matcher = re.search('.+/reviews/albums/(.+)/', url)
            id = matcher.group(1)
            print url + ',' + id
            out_file = data_dir + id + '.html'
            print out_file
            if not dry_run:
                os.system('wget -O %s -nc %s' % (out_file, url))
                time.sleep(2)
