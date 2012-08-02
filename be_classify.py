'''
Classify using bextract

@author: patrick
'''
from __future__ import division
import csv
import make_marsyas_col as util
from os import path
import os
import random
from sets import Set
import subprocess
import sys
import time

def main(genre, max_to_class, runname):
    reader = csv.reader(open(genre + '.csv', 'r'))
     
    indir = os.path.join(os.getcwd() + '/clips-by-score', genre + '_' + runname)
    resultspath = path.join(indir, 
        genre + '_' + runname + '_results_' + str(int(time.time())) + '.csv')
    resultfile = open(resultspath, 'w')
    writer = csv.writer(resultfile)
    writer.writerow(['Artist', 'Album', 'Score', 'clip', 'Predicted', 'Actual'])

    all_mp3s = []
    all_rows = []
    mp3_to_row_idx = {}
    for count, row in enumerate(reader):
        if count > 0:
            all_mp3s.extend(row[3:])
            
            for m in row[3:]:
                mp3_to_row_idx[m] = count
        all_rows.append(row)
            
    mp3s_in_class = []
    for f in os.listdir(indir):
        if f.endswith('.mf'):
            colreader = csv.reader(open(path.join(indir, f), 'r'), delimiter='\t')
            for row in colreader:
                if row: mp3s_in_class.append(row[0])
    
    mp3s_in_class = [path.basename(x) for x in mp3s_in_class]
    
    base_to_orig = {}
    all_mp3s_base = []
    for x in all_mp3s:
        base = path.basename(x)
        base_to_orig[base] = x
        all_mp3s_base.append(base)
    
    print mp3s_in_class
    print all_mp3s_base
    random.shuffle(all_mp3s_base)
    
    non_classed = list(Set(all_mp3s_base).difference(Set(mp3s_in_class)))
    random.shuffle(non_classed)

    procd = 0
    matched = 0
    for i in range(0, max_to_class):
        mp3 = base_to_orig[non_classed[i]]
        
        cmd = ["/home/patrick/apps/marsyas-0.4.5/build/bin/sfplugin", '-p',
               path.join(indir, genre + '_' + runname + '.mpl'), mp3]
        print ' '.join(cmd)
        
        proc = subprocess.Popen(cmd, cwd=indir, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        if stdout.find('Error') > -1 or stderr.find('Error') > -1:
            print 'Error for ', mp3
            print stdout
            print stderr
            print 'Proceeding'
            continue 
        conf_per_score = {'vg':0, 'g':0,'f':0,'p':0,'vp':0}
        for frame in stdout.split('\n'):
            elems = frame.split('\t')
            print elems
            if elems[0] != '':
                clss = elems[1]
                conf = int(elems[2])
                conf_per_score[clss] = conf_per_score[clss] + conf
        winning_conf = 0
        winning_clss = None
        for clss, conf in conf_per_score.iteritems():
            if conf > winning_conf:
                winning_conf = conf
                winning_clss = clss
        print conf_per_score
        idx = mp3_to_row_idx[mp3]
        
        row = all_rows[idx][0:3]
        print row
        actual = util.score_to_bin(int(row[2]))
        
        if winning_clss:
            row.append(mp3)
            row.append(winning_clss)
            row.append(actual)
            writer.writerow(row)
            print all_rows[idx]
            print('Prediction:', winning_clss, 'Actual:', actual)
            
            if winning_clss == actual:
                matched = matched + 1
            procd = procd + 1
                
        print 'stdout:', stdout
    print 'accuracy:', str(matched/procd)
    print 'Results at ', resultspath


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage:", sys.argv[0], 'genre max_to_class, runname'
    main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
