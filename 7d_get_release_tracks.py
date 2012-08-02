'''
Read release search responses (from 7 digital api) and use them
to get track listings (saving the responses).

@author: pmarchwiak
'''
import codecs
import csv
from lxml import etree
import os
import properties
import random
import requests
import sys
import time

def get_date_sorted_files(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a
    
def main(genre, start, end):
   
    indatadir = 'sevdig-data/release/search/' + genre
    outdatadir = 'sevdig-data/release/tracks/' + genre
   
    total = len(os.listdir(indatadir))
    
    for count, search_file_name in enumerate(get_date_sorted_files(indatadir)):
        if count >= start and count <= end:
            print 'processing release %d/%d' % (count, total)
            xmlstr = codecs.open(os.path.join(indatadir, search_file_name), 'r', 'utf-8').read()
            # lxml doesn't like the encoding for some reason
            xmlstr = xmlstr.replace(' encoding="utf-8"', '')
            root = etree.fromstring(xmlstr)
            releases = root.findall('searchResults/searchResult/release')
            release_id = None
            for release in releases:
                 artist = release.find('artist/name').text
                 album = release.find('title').text
                 if (artist + ' ' + album).replace(' ', '_'). \
                        replace('/', '').strip() + '.xml' == search_file_name:
                     release_id = release.get('id')
                     break
           
            if release_id: 
                r = requests.get(properties.sevdig_api+'/release/tracks',
                    params={'country':'US', 'releaseid':release_id,
                    'oauth_consumer_key': properties.sevdig_key})
              
                if not os.path.exists(outdatadir):
                    os.makedirs(outdatadir)
                    
                track_file_name = release_id + '-' + album.replace('/',' ') + '.xml'
                track_file = codecs.open(os.path.join(outdatadir, track_file_name), 'w', 'utf-8')
                track_file.write(r.content)
                track_file.close()
                print 'wrote ' + track_file_name
                
                rate_headers = ['x-ratelimit-limit', 'x-ratelimit-current', 'x-ratelimit-reset']
                for h in rate_headers:
                    print h + ": " + r.headers[h]
                sec = int(r.headers['x-ratelimit-reset'])
                min = sec / 60
                hrs = min / 60
                min = str(min % 60)
                if len(min) == 1: min = '0' + min
                print "time left till next period: %d:%s" % (hrs, min)
                #time.sleep(random.randrange(3,7))
                time.sleep(2)
            else:
                print 'No matching release found'
        
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print "Usage: " + sys.argv[0] + " genre start_row end_row"
        sys.exit(1)
        
    main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
