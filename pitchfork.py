"""Pitchfork.com 
"""

__author__ = 'pd@marchwiak.com (Patrick Marchwiak)'


from bs4 import BeautifulSoup
from datetime import datetime
import re
import sys
import urllib2


BASE_URL = 'http://pitchfork.com'

class Review(object):
    """Represents a review
    
    Attributes:
        id
        text: the review text
        score: the score on a scale of 0-10
        artist: the name of the artist
        date: datetime object for review date
    """
    id = None
    text = ''
    score = None
    artist = ''
    date = None
    album = ''

    def __str__(self):
        return "artist: %s, album: %s, %f" % (self.artist,
            self.album, self.score)

def search_albums(search_term):
    """Find albums that match the search term
    
    Args:
        search_term

    Returns:
        list of urls relative to BASE_URL
    """
    resp = urllib2.urlopen('%s/search/more/?filter=album_reviews&query=%s' % 
        (BASE_URL, search_term))
    return _parse_search_albums_html(resp)

def _parse_search_albums_html(resp):
    soup = BeautifulSoup(resp)
    urls = [a['href'] for a in soup.find("div", "search-group").find_all("a")]
    return urls

def get_review(url):
    """Parses review for the given relative url
    
    Args:
        url: album url relative to BASE_URL

    Returns:
        Review object
    """
    resp = urllib2.urlopen(BASE_URL + url)
    return _parse_review_html(resp)
    
def _parse_review_html(resp):
    soup = BeautifulSoup(resp)
    rev = None
    try:
        meta = soup.find('ul', "review-meta")
        rev = Review()
        # rev.id = int(re.search('\d+', relpath).group(0))
        rev.artist = meta.find('h1').find('a').get_text()
        rev.album = meta.find('h2').get_text()
        str_date = meta.find('span', "pub-date").get_text()
        rev.date = datetime.strptime(str_date, '%B %d, %Y')
        rev.score = float(meta.find('span', "score").get_text())
        rev.text = soup.find('div', 'editorial').get_text()

    except Exception as e:
        print e

    return rev

    
if __name__ == '__main__':
    print get_review(search_albums(sys.argv[1])[0])
