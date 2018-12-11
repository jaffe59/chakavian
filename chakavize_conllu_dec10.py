#TODO: some words get deleted after running this code: PUNCT, CCONJ, ADV, ADP, ADJ, NOUN
#TODO: decide how to take care of "language-neutral" PUCNT, SYM, etc.
#TODO: train split

#process verbal Cakavian endings from standard Croatian train
#masc. past particple no -o.  for i before infinitive: raditi  -> radi/radi(j)a vs. standard radio
#                             no  i before infinitive: postati -> posta         vs. standard postao 
#                                                      gledati -> gleda         vs. standard gledao 
#present 3rd plural. -du or -u vs. standard -u, -ju, -e.
#                             e.g., pusu/pusidu vs. standard puse, 
#                                        crtadu vs. standard crtaju, 
#                                       plesedu vs. standard plesu

#input conllu train line by line - change matching entries to their Cakavian inflections
#leave non-matching entries the same

import sys
import re

def is_plural_genitive(line):
    # word number, full_form, lemma, pos, ?, features, governor_index, deplabel, _, space_after
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    if pos == "NOUN" and "Case=Gen" in features and "Number=Plur" in features:
        return True
    return False

def is_datlocins_plural(line):
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    if pos == "NOUN" and "Number=Plur" in features and "Case=Dat" in features or\
            pos == "NOUN" and "Number=Plur" in features and "Case=Loc" in features or \
            pos == "NOUN" and "Number=Plur" in features and "Case=Ins" in features:
        return True
    return False

def is_masc_past_part(line):
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    if "Gender=Masc" in features and "Tense=Past" in features and "VerbForm=Part" in features:
        return True
    else:
        return False

def is_3rd_plural(line):
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    if "Tense=Pres" in features and "Person=3" in features and "Number=Plur" in features:
        return True
    else:
        return False

def inflect_mpp(line):
    #masc. past particple no -o.  for i before infinitive: raditi  -> radi/radi(j)a vs. standard radio
    #                             no  i before infinitive: postati -> posta         vs. standard postao 
    #                                                      gledati -> gleda         vs. standard gledao 
    #if ends in iti, goes to i or ia or ija
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    fields = line.split()
    if lemma == "biti": #ignore copula probably irregular
        features += "|Dialect=Sto"
        fields[5] = features
        return " ".join(fields)
    if lemma.endswith("iti") and full_form[-1] == 'o':
        #TODO choose one, or all? of these
        #full_form = full_form[:-1]       #final o deletion
        #full_form = full_form[:-1] + "a" #swap o with a
        full_form = full_form[:-1] + "ja" #swap o with ja
        features += "|Dialect=Cha"
    elif full_form[-1] == 'o' or full_form[-1] == 'O': #else remove -o of full shtokavian form
        full_form = full_form[:-1]      #remove final o
        features += "|Dialect=Cha"
    elif lemma.endswith("iti") and full_form[-1] == 'O':
        full_form = full_form[:-1] + "JA" #swap o with ja
        features += "|Dialect=Cha"
    else:
        print("unexpected mpp - {} {} {}".format(full_form, lemma, features))
        features += "|Dialect=Sto"
    fields[1] = full_form
    fields[5] = features
    return " ".join(fields)

def inflect_3pp(line):
    #present 3rd plural. -du or -u vs. standard -u, -ju, -e.
    #                             e.g., pusu/pusidu vs. standard puse, 
    #                                        crtadu vs. standard crtaju, 
    #                                       plesedu vs. standard plesu
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    fields = line.split()
    if lemma == "biti":
        features += "|Dialect=Sto"
        fields[5] = features
        return " ".join(fields)
    #identify standard class -u, -ju, -e
    if full_form.endswith("ju"):
        full_form = full_form[:-2]+"du" #-ju becomes -du?
        features += "|Dialect=Cha"
    elif full_form.endswith("e"):
        #TODO choose one of these?
        full_form = full_form[:-1]+"u" #-e becomes -u?
        #full_form = full_form[:-1]+"idu" #-e becomes -idu?
        features += "|Dialect=Cha"
    elif full_form.endswith("u"):
        full_form = full_form[:-1]+"edu" #-u becomes -edu?
        features += "|Dialect=Cha"
    #CAPS
    elif full_form.endswith("JU"):
        full_form = full_form[:-2]+"DU" #-ju becomes -du?
        features += "|Dialect=Cha"
    elif full_form.endswith("E"):
        full_form = full_form[:-1]+"U" #-e becomes -u?
        features += "|Dialect=Cha"
    elif full_form.endswith("U"):
        full_form = full_form[:-1]+"EDU" #-u becomes -edu?
        features += "|Dialect=Cha"
    else:
        print("unexpected 3pp - {} {} {}".format(full_form, lemma, features))
        features += "|Dialect=Sto"
    fields[1] = full_form
    fields[5] = features
    return " ".join(fields)

def inflect_genplural(line):
    full_form_exceptions = ["djece"]
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    fields = line.split()
    if full_form in full_form_exceptions:
        features += "|Dialect=Sto"
        fields[5] = features
        return " ".join(fields)
    else:
        if re.search('Masc', features) is not None:
            full_form = full_form[:-1] + 'i'
            features += "|Dialect=Cha"
        # fem/neut: zero ending on the root in contrast to standard -a
        elif full_form[-1] == 'a':
            full_form = full_form[:-1]
            features += "|Dialect=Cha"
        elif full_form[-1] == 'i':
            features += "|Dialect=Sto"
        else:
            print("unexpected genpl - {} {} {}".format(full_form, lemma, features))
            features += "|Dialect=Sto"
        fields[1] = full_form
        fields[5] = features
        return " ".join(fields)

def inflect_dli_plural(line):
    _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
    fields = line.split()
    if full_form[-3:] == 'ima':
        full_form += 'n'
        features += "|Dialect=Cha"
    # replace -ma with -n (for 'a' nouns)
    elif full_form[-3:] == 'ama':
        full_form = full_form[:-2] + 'n'
        features += "|Dialect=Cha"
    else:
        print("unexpected dlipl - {} {} {}".format(full_form, lemma, features))
        features += "|Dialect=Sto"
    fields[1] = full_form
    fields[5] = features
    return " ".join(fields)

def main():
    #create input and output file handles
    iff = open(sys.argv[1], 'r')
    off = open(sys.argv[2], 'w+')

    for line in iff:
        if "sent_id" in line or line == "\n" or "text = " in line:
            off.write(line)
            continue
        if is_masc_past_part(line):
            off.write(inflect_mpp(line))
            continue
        if is_3rd_plural(line):
            off.write(inflect_3pp(line))
            continue
        if is_plural_genitive(line):
            off.write(inflect_genplural(line))
            continue
        if is_datlocins_plural(line):
            off.write(inflect_dli_plural(line))
            continue
        else:
            _, full_form, lemma, pos, _, features, _, _, _, _ = line.split()
            fields = line.split()
            features += "|Dialect=Sto"
            fields[5] = features
            off.write(" ".join(fields)+"\n")

if __name__ == "__main__":
    main()
