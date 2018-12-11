# chakavian
requires MED-pytorch
requires pytorch-seq2seq

1. lowercase conll data with "lowerCase_firsttwo_conllu.py"
2. "chakavize" to reinflect 4 target forms with "chakavize_conllu.py".
3. do data split, interleaving lowered conll and lowered chakavized_conll
4. preprocess to generate MED-format input data with "preprocess_conllu.py", creating vocab.source and vocab.target for each medformat file produced
5. subsample medformat files to generate smaller training files with "subsample <filename> <p>" e.g., get 10% of data with 0.1 for your p
