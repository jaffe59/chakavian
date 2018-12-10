#lower conllu to re-tagged lower conllu

import sys
import re

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
    return " ".join(fields)

def main():
    iff = open(sys.argv[1], 'r')
    tag = sys.argv[2]
    offdia = open(sys.argv[1]+"."+tag, 'w')

    for line in iff:
        if line.startswith("#") or line == "\n": #write non-data lines in all files without sampling
            offdia.write(line)
        else:
            offdia.write(set_dia(line,tag)+"\n")

    offdia.close()

if __name__ == "__main__":
    main()


