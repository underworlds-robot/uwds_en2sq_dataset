#!/bin/bash
if [ $# -eq 0 ]
then
    echo "usage: $0 \"<sentence_to_translate>\" The inference may take a while (due to model loading...)"
    exit 1
fi

echo $1 > src-test.txt

onmt-main infer --config config.yml --auto_config --features_file src-test.txt > tgt-test.txt

cat tgt-test.txt
