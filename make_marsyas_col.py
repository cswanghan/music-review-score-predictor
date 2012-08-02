'''
Build marsyas collections based on score

@author: patrick
'''
import csv
import os
import random
import subprocess
import sys

vg = range(81,101)
g = range(61,81)
f = range(40,61)
p = range(20,40)
vp = range(0,20)

def score_to_bin(score):
    if score in vg:
        return 'vg'
    elif score in g:
        return 'g'
    elif score in f:
        return 'f'
    elif score in p:
        return 'p'
    elif score in vp:
        return 'vp'
    
def main(genre, max_col_size, runname):
    reader = csv.reader(open(genre + '.csv', 'r'))
   
    outdir = os.path.join(os.getcwd() + '/clips-by-score', genre + '_' + runname)
    if os.path.exists(outdir):
        print outdir, 'already exists'
        sys.exit(1)
    else:
        os.makedirs(outdir)
  
    mp3s_by_score = {} 
    
    missing = 0 
    for count, row in enumerate(reader):
        print 'missing:', missing
        if count == 0:
            continue
        
        artist = row[0]
        album = row[1]
        score = int(row[2])
        mp3s = row[3:]
        print row
       
        bin = score_to_bin(score)
        if not bin:
            print 'invalid bin for ', row
            sys.exit(1)
        print 'bin', bin
        if bin in mp3s_by_score:
            mp3s_by_score[bin].extend(mp3s)
        else:
            mp3s_by_score[bin] = mp3s
      
#    print mp3s_by_score
    os.chdir(outdir)
    for bin, mp3s in mp3s_by_score.iteritems():
        print outdir, bin
        bindir = os.path.join(outdir, bin)
        os.makedirs(bindir)
        count = 0
        random.shuffle(mp3s)
        for count, mp3 in enumerate(mp3s):
            if count > max_col_size:
                break
            os.link(mp3, os.path.join(bindir, os.path.basename(mp3)))
        
        cmd = ["/home/patrick/apps/marsyas-0.4.5/build/bin/mkcollection", '-l',
               bin, '-c', genre + '_' + bin, bindir]
        
        proc = subprocess.Popen(cmd, cwd=outdir)
        proc.wait()
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage:", sys.argv[0], 'genre max_col_size runname'
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    
