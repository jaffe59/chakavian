import sys
import re
import random
import pdb

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

    #reading two input files
    standardf = open(sys.argv[1],'r')
    localf = open(sys.argv[2],'r')
    standardlines = standardf.readlines()
    locallines = localf.readlines()
    standardf.close()
    localf.close()
    assert len(locallines) == len(standardlines)

    #do:
    #100   standard
    #75/25 standard/local
    #50/50 standard/local
    #25/75 standard/local
    #100   local

    #open 6 output files by data split
    off100s = open(sys.argv[1]+".100s", 'w')
    off75s = open(sys.argv[1]+".75s", 'w')
    off50s = open(sys.argv[1]+".50s", 'w')
    off25s = open(sys.argv[1]+".25s", 'w')
    off0s = open(sys.argv[1]+".0s", 'w')

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

            if flip(0.75):
                off75s.write(set_dia(standardline,"Sto")) #choose standard 75% of time
            else:
                off75s.write(set_dia(localline,"Cha")) #choose local 25% of time 

            if flip(0.5):
                off50s.write(set_dia(standardline,"Sto")) #choose standard 50% of time
            else:
                off50s.write(set_dia(localline,"Cha")) #choose local 50% of time 

            if flip(0.25):
                off25s.write(set_dia(standardline,"Sto")) #choose standard 25% of tiem
            else:
                off25s.write(set_dia(localline,"Cha")) #choose local 75% of time 
                
            off0s.write(set_dia(localline,"Cha")) #choose local 100% of time

    off100s.close()
    off75s.close()
    off50s.close()
    off25s.close()
    off0s.close()

if __name__ == "__main__":
    main()

