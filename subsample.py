#subsample medformat files where each line has probability p of being kept
#Usage: python <thisfile> <targetfile> <p>
import random
import sys

def flip(p):
    return True if random.random() < p else False 

def main():
    fn = sys.argv[1]
    p = float(sys.argv[2])
    with open(fn, 'r') as iff:
        with open(fn+".sub"+str(p), 'w') as off:
            for line in iff:
                if flip(p):
                    off.write(line)

if __name__ == "__main__":
    main()





