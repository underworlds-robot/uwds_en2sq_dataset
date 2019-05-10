# uwds_en2sq_dataset

The dataset used to learn how to translate NL query to SPARQL.

This repository include a simple dataset generator to be used by [OpenNMT](http://opennmt.net/OpenNMT-tf/index.html) !

### Installation instructions

```shell
git clone https://github.com/underworlds-robot/uwds_en2sq_dataset.git
cd uwds_en2sq_dataset
pip install -r --user requirements.txt
```

### Generate the dataset

In order to generate the Underworlds dataset, open a shell and type :
```shell
cd uwds_en2sq_dataset
python generator.py --templates <your_templates> --individuals <your_individuals> --examples\_per\_template <nb_ex_per_template>
```

### Create your own dataset

#### Templates

The aim of this file is to describe data pairs as templates of sentence and query where the `<A>`, `<B>`, `<C>` variables are then replaced by the given individuals.
To know which individuals to choose, the type is described in the 3 first lines !

#### Individuals

This file describe the possible individuals given the individuals type.

### References

This generator have been inspired by this project :
* [SPARQL as a Foreign Language](https://arxiv.org/abs/1708.07624)
* [https://github.com/dbpedia/neural-qa](https://github.com/dbpedia/neural-qa)