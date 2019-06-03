#!/usr/bin/env python

import argparse
import csv
import numpy as np

np.random.seed(123)  # for reproducibility

def build_vocab(target_file_path, glove_file_path="res/data/glove/glove.6B.50d.txt", stop_list=50000):
    vocab = {}
    token_by_index = {}
    index = 0
    with open(glove_file_path, "r") as glove_file:
        for row in glove_file:
            if index > stop_list:
                break
            token = row.split(" ")[0]
            try:
                test = token.replace("-", "")
                test = float(test)
            except ValueError:
                vocab[token] = index
                token_by_index[index] = token
                index += 1

    with open(target_file_path, "r") as tgt_file:
        for row in tgt_file:
            for token in row.split():
                if token not in vocab:
                    vocab[token] = index
                    token_by_index[index] = token
                    index += 1

    with open("src-vocab.txt", "w") as src_vocab_file:
        with open("tgt-vocab.txt", "w") as tgt_vocab_file:
            tgt_vocab_file.write("<blank>\r\n<s>\r\n</s>\r\n")
            src_vocab_file.write("<blank>\r\n<s>\r\n</s>\r\n")
            for i in range(0, len(token_by_index)):
                if token_by_index[i]!="":
                    tgt_vocab_file.write(str(token_by_index[i])+"\r\n")
                    src_vocab_file.write(str(token_by_index[i])+"\r\n")

def load_templates(templates_file_path):
    variables_by_index = {}
    templates_by_index = {}
    index = 0
    with open(templates_file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_line = next(reader)
        nb_variables = len(first_line) - 2
    with open(templates_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            variables_by_index[index] = []
            templates_by_index[index] = {}
            for i in range(0, nb_variables):
                if row[str(chr(65+i))] != "":
                    variables_by_index[index].append(row[str(chr(65+i))])
            templates_by_index[index]["source"] = row["source"]
            templates_by_index[index]["target"] = row["target"]
            index += 1
    return variables_by_index, templates_by_index

def load_individuals(templates_file_path):
    individuals_map = {}
    with open(templates_file_path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_line = next(reader)
        for individuals_type in first_line:
            individuals_map[individuals_type] = []
    with open(templates_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            for type in first_line:
                if type in row:
                    if row[type] != "":
                        individuals_map[type].append(row[type])
    return individuals_map

def generate_data_pairs(variables, templates, individuals, nb_examples_per_template=600):
    pairs = []
    already_generated = {}
    for i in range(0,len(templates)):
        print ("Generation of the "+str(i)+"th template...")
        for j in range(0, nb_examples_per_template):
            variables_list = variables[i]
            source = templates[i]["source"]
            target = templates[i]["target"]
            source, target = generate_random_pair(variables_list, source, target, individuals)
            if source not in already_generated:
                pairs.append((source, target))
            already_generated[source] = True
    return pairs

def generate_random_pair(variables, source, target, individuals):
    pairs = []
    if len(variables) > 0:
        for i in range(0, len(variables)):
            index = pick_index(individuals[variables[i]])
            target = target.replace(".", ",")
            target = target.replace("<"+str(chr(65+i))+">", individuals[variables[i]][index])
            source = source.replace("<"+str(chr(65+i))+">", individuals[variables[i]][index])
    return source, target

def pick_index(sequence):
    return int((np.random.random_sample() * len(sequence)) % len(sequence))

def save(data_pairs, source_file_path, target_file_path, source_val_file_path, target_val_file_path):
    with open(source_file_path, 'w') as src_file:
        with open(target_file_path, 'w') as tgt_file:
            with open(source_val_file_path, 'w') as src_val_file:
                with open(target_val_file_path, 'w') as tgt_val_file:
                    nb_train = 0
                    nb_val = 0
                    for data_pair in data_pairs:
                        source, target = data_pair
                        if np.random.random_sample() > 0.1:
                            src_file.write(source + "\r\n")
                            tgt_file.write(target + "\r\n")
                            nb_train += 1
                        else:
                            src_val_file.write(source + "\r\n")
                            tgt_val_file.write(target + "\r\n")
                            nb_val += 1
                    print ("Saved "+str(nb_train)+" pairs in training dataset : "+source_file_path+" "+target_file_path)
                    print ("Saved "+str(nb_val)+" pairs in validation dataset : "+source_val_file_path+" "+target_val_file_path)

def main(templates_file_path="templates.csv", individuals_file_path="individuals.csv", max_examples_per_template=600, output_en_file="src-train.txt", output_sq_file="tgt-train.txt", src_val_file="src-val.txt", tgt_val_file="tgt-val.txt"):
    variables, templates = load_templates(templates_file_path)
    individuals = load_individuals(individuals_file_path)
    pairs = generate_data_pairs(variables, templates, individuals, max_examples_per_template)
    print (str(len(pairs))+" data pairs generated from "+str(len(templates))+" templates ! Enjoy !")
    save(pairs, output_en_file, output_sq_file, src_val_file, tgt_val_file)
    build_vocab(output_sq_file)
    print ("Bye bye !")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The dataset generator.')
    parser.add_argument("--templates", type=str, default="templates.csv", help='The templates file to use')
    parser.add_argument("--individuals", type=str, default="individuals.csv", help='The individuals to randomly pick')
    parser.add_argument("--examples_per_template", type=int, default=600, help="The max number of examples to generate per template")

    args = parser.parse_args()
    print ("Start generating dataset...")
    main(templates_file_path=args.templates, individuals_file_path=args.individuals, max_examples_per_template=args.examples_per_template)
