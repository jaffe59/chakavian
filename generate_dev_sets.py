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

def get_training_vocab(training_file):
    lemmas = Set()
    full_form_targets = Set()
    for line in training_file:
        if (not line.startswith("#")) and line != '\n':
            _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
            lemmas.add(lemma)
            full_form_targets.add(full_form)
    return lemmas, full_form_targets


def main():
    iff = open(sys.argv[1], 'r')
    tag = sys.argv[2]
    training_file = sys.argv[3]
    offdia = open(sys.argv[1]+"."+tag, 'w')

    lemma_filter_set, full_form_filter_set = get_training_vocab(training_file)

    for line in iff:
        if line.startswith("#") or line == "\n": #write non-data lines in all files without sampling
            offdia.write(line)
        else:
            _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
            if lemma not in lemma_filter_set: #filter dev items to only include lemmas not seen in training. strongest filter.  could ease back to full form if this reduces the dev set too much.  high-frequency items will be filtered, which may impact dev representativeness, but makes the test harder and more ecologically viable
                offdia.write(set_dia(line,tag)+"\n")

    offdia.close()

if __name__ == "__main__":
    main()


