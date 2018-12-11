import sys
import re
import random
import pdb
from collections import Counter

def sample_and_write_output(standardline, localline, p, off, stats_tracker):
    '''
    Choose standard dialect tag with probability p.  
    Then, separate choice of form to use with probability p.  
    I.e., two separate Bernoulli trials for sample dialect tag and form to use.  
    Then, write the line to file. 
    Also, for reinflected forms, counts how often there's mismatch
    '''
    if flip(p): #flip for dialect tag
        tag = "Sto"
    else:
        tag = "Cha"
    if flip(p): #flip for form used
        line = standardline
    else:
        line = localline
    off.write(set_dia(line, tag))

    if standardline != localline: #get stats for reinflected lines
        if tag == "Sto" and line == standardline:
            stats_tracker['stotag_stoform'] += 1
        if tag == "Sto" and line == localline:
            stats_tracker['stotag_chaform'] += 1
        if tag == "Cha" and line == standardline:
            stats_tracker['chatag_stoform'] += 1
        if tag == "Cha" and line == localline:
            stats_tracker['chatag_chaform'] += 1

def flip(p):
    return True if random.random() < p else False 

def set_dia(line,tag):
    '''
    takes 10field conll line.  
    removes any dialect tags.
    adds "Dialect=tag" to features field, where tag is supplied 
    '''
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    fields = line.split()
    if "Dialect" in features:
        features = re.sub('Dialect=...\|?', '', features) #remove Dialect=xxx and optional trailing delimiter
    features += "|Dialect="+tag #append new Dialect tag
    fields[5] = features
    return " ".join(fields)+"\n"

def main():
    '''
    read in two input files, generate splits interleaving forms and tags, using separate bernoulli trials. 
    also print stats on reinflected forms for the splits
    '''

    #reading two input files
    standardf = open(sys.argv[1],'r')
    localf = open(sys.argv[2],'r')
    standardlines = standardf.readlines()
    locallines = localf.readlines()
    standardf.close()
    localf.close()
    assert len(locallines) == len(standardlines)

    #open 6 output files by data split
    off100s = open(sys.argv[1]+".100s", 'w')
    off75s  = open(sys.argv[1]+".75s",  'w')
    off50s  = open(sys.argv[1]+".50s",  'w')
    off25s  = open(sys.argv[1]+".25s",  'w')
    off0s   = open(sys.argv[1]+".0s",   'w')

    stats_100s = Counter()
    stats_75s = Counter()
    stats_50s = Counter()
    stats_25s = Counter()
    stats_0s = Counter()

    for i in range(len(locallines)):
        standardline = standardlines[i]
        localline = locallines[i]
        if standardline.startswith("#") or standardline == "\n": #write non-data lines in all files without sampling
            off100s.write(standardline)
            off75s.write(standardline)
            off50s.write(standardline)
            off25s.write(standardline)
            off0s.write(standardline)
        else:
            off100s.write(set_dia(standardline,"Sto")) #choose standard 100% of time
            if standardline != localline: #stats for 100s reinflected forms
                stats_100s['stotag_stoform'] += 1
                stats_0s['chatag_chaform'] += 1

            sample_and_write_output(standardline, localline, 0.75, off75s, stats_75s)
            sample_and_write_output(standardline, localline, 0.5, off50s, stats_50s)
            sample_and_write_output(standardline, localline, 0.25, off25s, stats_25s)

            off0s.write(set_dia(localline,"Cha")) #choose local 100% of time
            

    off100s.close()
    off75s.close()
    off50s.close()
    off25s.close()
    off0s.close()

    print("100s stats: reinflected forms count: {}".format(stats_100s['stotag_stoform']))
    print("75s stats: " + str(stats_75s))
    print("50s stats: " + str(stats_50s))
    print("25s stats: " + str(stats_25s))
    print("0s stats: reinflected forms count: {}".format(stats_0s['chatag_chaform'])) #not really necessary but sanity check they're the same as the 100s stats

if __name__ == "__main__":
    main()
