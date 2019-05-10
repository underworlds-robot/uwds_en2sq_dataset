#!/usr/bin/env python

import argparse
import csv
import numpy as np

np.random.seed(123)  # for reproducibility

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
                if row["var "+str(chr(65+i))] != "":
                    variables_by_index[index].append(row["var "+str(chr(65+i))])
            templates_by_index[index]["sentence"] = row["sentence"]
            templates_by_index[index]["query"] = row["query"]
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
            sentence = templates[i]["sentence"]
            query = templates[i]["query"]
            sentence, query = generate_random_pair(variables_list, sentence, query, individuals)
            if sentence not in already_generated:
                pairs.append((sentence, query))
            already_generated[sentence] = True
    return pairs

def generate_random_pair(variables, sentence, query, individuals):
    pairs = []
    if len(variables) > 0:
        for i in range(0, len(variables)): 
            index = pick_index(individuals[variables[i]])
            query = query.replace(".", ",")
            query = query.replace("<"+str(chr(65+i))+">", individuals[variables[i]][index])
            sentence = sentence.replace("<"+str(chr(65+i))+">", individuals[variables[i]][index])
    return sentence, query

def pick_index(sequence):
    return int((np.random.random_sample() * len(sequence)) % len(sequence))

def save(data_pairs, source_file_path, target_file_path):
    with open(source_file_path, 'w') as src_file:
        with open(target_file_path, 'w') as tgt_file:
            for data_pair in data_pairs:
                sentence, query = data_pair
                src_file.write(sentence + "\r\n")
                tgt_file.write(query + "\r\n")

def main(templates_file_path="templates.csv", individuals_file_path="individuals.csv", nb_examples_per_template=600, output_en_file="src-train.txt", output_sq_file="tgt-train.txt"):
    variables, templates = load_templates(templates_file_path)
    individuals = load_individuals(individuals_file_path)
    pairs = generate_data_pairs(variables, templates, individuals, nb_examples_per_template)
    save(pairs, output_en_file, output_sq_file)
    print (str(len(pairs))+" data pairs generated from "+str(len(templates))+" templates ! Enjoy !")
    print ("Bye bye !")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The dataset generator.')
    parser.add_argument("--templates", type=str, default="templates.csv", help='The templates file to use')
    parser.add_argument("--individuals", type=str, default="individuals.csv", help='The individuals to randomly pick')
    parser.add_argument("--examples_per_template", type=int, default=600, help="The number of examples to generate per template")

    args = parser.parse_args()
    print ("Start generating dataset...")
    main(templates_file_path=args.templates, individuals_file_path=args.individuals, nb_examples_per_template=args.examples_per_template)

