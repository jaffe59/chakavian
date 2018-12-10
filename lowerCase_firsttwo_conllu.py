import sys
import pdb

with open(sys.argv[1], 'r') as iff:
    try:
        for line in iff:
            if line.startswith("#") or line == "" or line == "\n":
                sys.stdout.write(line)
            else:
                fields = line.split()
                fields[1] = fields[1].lower()
                fields[2] = fields[2].lower()
                sys.stdout.write(" ".join(fields)+"\n")
    except:
        pdb.set_trace()


