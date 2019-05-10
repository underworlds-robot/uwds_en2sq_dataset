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
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            variables_by_index[index] = []
            templates_by_index[index] = {}
            if row["var A"] != "":
                variables_by_index[index].append(row["var A"])
            if row["var B"] != "":
                variables_by_index[index].append(row["var B"])
            if row["var C"] != "":
                variables_by_index[index].append(row["var C"])
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
        print individuals_map
    with open(templates_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            print row
            for type in first_line:
                if type in row:
                    if row[type] != "":
                        individuals_map[type].append(row[type])
    return individuals_map

def generate_data_pairs(variables, templates, individuals, nb_examples_per_template=600):
    pairs = []
    is_unique = {}
    for i in range(0,len(templates)):
        print "Generation of the "+str(i)+"th template..."
        for j in range(0, nb_examples_per_template):
            variables_list = variables[i]
            sentence = templates[i]["sentence"]
            query = templates[i]["query"]
            # Check if already generated ?
            pairs.append(generate_random_pair(variables_list, sentence, query, individuals))
    return pairs

def generate_random_pair(variables, sentence, query, individuals):
    pairs = []
    if len(variables) > 0:
        index = pick_index(individuals[variables[0]])
        query.replace(".", ",")
        query = query.replace("<A>", individuals[variables[0]][index])
        sentence = sentence.replace("<A>", individuals[variables[0]][index])
        if len(variables) > 1:
            index = pick_index(individuals[variables[1]])
            query = query.replace("<B>", individuals[variables[1]][index])
            sentence = sentence.replace("<B>", individuals[variables[1]][index])
            if len(variables) > 2:
                index = pick_index(individuals[variables[2]])
                query = query.replace("<C>", individuals[variables[2]][index])
                sentence = sentence.replace("<C>", individuals[variables[2]][index])
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
    print variables
    print templates
    individuals = load_individuals(individuals_file_path)
    print individuals
    pairs = generate_data_pairs(variables, templates, individuals, nb_examples_per_template)
    save(pairs, output_en_file, output_sq_file)
    print "Bye bye !"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='The dataset generator.')
    parser.add_argument("--templates", type=str, default="templates.csv", help='The templates file to use')
    parser.add_argument("--individuals", type=str, default="individuals.csv", help='The individuals to randomly pick')
    parser.add_argument("--examples_per_template", type=int, default=600, help="The number of examples to generate per template")

    args = parser.parse_args()
    print "Generating dataset..."
    main(templates_file_path=args.templates, individuals_file_path=args.individuals, nb_examples_per_template=args.examples_per_template)

