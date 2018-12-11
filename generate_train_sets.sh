# use python3 for non-ASCII support

#lower-case training data
python lowerCase_firsttwo_conllu.py data/train/hr_set-ud-train.conllu > data/train/hr_set-ud-train.lower.conllu

#reinflect to create chakavized dataset
python chakavize_conllu.py data/train/hr_set-ud-train.lower.conllu data/train/hr_set-ud-train.lower.chakavized.conllu 

#generate data splits 0s, 25s, 50s, 75s, 100s
python interleave_datasets_and_label_dialect.py data/train/hr_set-ud-train.lower.conllu data/train/hr_set-ud-train.lower.chakavized.conllu 

#make dirs, convert to medformat, move vocab.source and vocab.target to dir, then subsample
for i in 0s 25s 50s 75s 100s; do 
    mkdir -p data/${i}
    python preprocess_conllu.py data/train/hr_set-ud-train.lower.conllu.${i} data/${i}/hr_set-ud-train.lower.conllu.${i}.medformat
    mv vocab* data/${i}/.
    python subsample.py data/${i}/hr_set-ud-train.lower.conllu.${i}.medformat 0.1
done



