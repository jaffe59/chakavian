import sys, os


def clean_lines(line):
    # need to fix list length to 6 to avoid IndexError
    # feature set
    out = 'OUT='
    pos = 'pos='
    featset = [out + pos + line[3]]
    for feat in line[5].replace('|', ' ').split():
        if feat != '_':
            feat = out + feat
            feat = feat.strip()
            featset.append(feat)
    # lemma (line[2]) and inflected form (line[1])
    lemma = []
    infl = []
    for char in line[2]:
        lemma.append(char)
    for char in line[1]:
        infl.append(char)
    # how to join the list can be revised as necessary
    return ' '.join(featset) + ' ' + ' '.join(lemma) + '\t' + ' '.join(infl)


def main():
    # create input and output file handles
    iff = open(sys.argv[1], 'r').readlines()
    off = open(sys.argv[2], 'w+')
    src_vocab = open('vocab.source', 'w')
    tgt_vocab = open('vocab.target', 'w')

    src_seen = {}
    src_uniq = []
    tgt_seen = {}
    tgt_uniq = []

    for line in iff:
        # chakavize.py joins the list with a space, not \t
        splitline = line.split()[0:6]
        if "PUNCT" not in line:
            if len(splitline) == 6 and splitline[0] != '#':
                off.write(clean_lines(splitline) + '\n')

                tabsplit = clean_lines(splitline).split("\t")

                for char in tabsplit[0].split():
                    if char in src_seen:
                        continue
                    src_seen[char] = 1
                    src_uniq.append(char)

                for char in tabsplit[1].split():
                    if char in tgt_seen:
                        continue
                    tgt_seen[char] = 1
                    tgt_uniq.append(char)

    for a in src_uniq:
        src_vocab.write(str(a) + '\n')
    for a in tgt_uniq:
        tgt_vocab.write(str(a) + '\n')

if __name__ == "__main__":
    main()

