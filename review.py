class Review(object):
    id = None
    text = ''
    score = None
    artist = ''
    date = None
    album = ''

    def __str__(self):
        return "artist: %s, album: %s, %f" % (self.artist,
            self.album, self.score)

    def arff_header(self):
        header = """@RELATION reviews

@attribute id numeric
@attribute artist string
@attribute album string
@attribute score numeric
@attribute date date
@attribute text string
        
@data
"""
        return header
    
    def arff_row(self):
        return "%d, '%s','%s',%f,%s,'%s'\n" % (self.id, arff_escape(self.artist),
            arff_escape(self.album), self.score, self.date.isoformat(),
            arff_escape(self.text))