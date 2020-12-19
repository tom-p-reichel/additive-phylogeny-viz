# Additive Phylogeny Visualizer

This repo contains an implementation of the additive phylogeny algorithm as well as a couple application scripts.

# Dependencies

 - recent Python 3 version
 - graphviz (dot must be on the path)
 - numpy
 - matplotlib (for benchmark)

# `additive_phylogeny.py`
This file contains the implementation of the additive phylogeny algorithm, implemented with utilities from the `utilities.py` file. Running it will run unit tests, which may take some time! The program should terminate without error.

# `demo.py`
This file is a front-end to `additive_phylogeny.py` that generates a phylogeny from a given additive distance matrix. A distance matrix can be passed into the program via a `.csv`, or a random additive distance matrix of a certain size can be generated. The program renders the incremental building of the tree into a given output directory as a series of `.png`'s.
```
usage: demo.py [-h] [--n N] [--csv CSV] outputdir

positional arguments:
  outputdir   a directory in which to place frames of the additive phylogeny algorithm

optional arguments:
  -h, --help  show this help message and exit
  --n N       number of leaf nodes in randomly generated tree
  --csv CSV   a headerless csv file containing a distance matrix from which to generate an additive phylogeny

```
This information is available on the command line as well, via `python demo.py -h`.

# `bench.py`
This program runs a benchmark of the algorithm, and then fits polynomials to the runtime via least squares regression. It shows the resultant figure using matplotlib.

```
usage: bench.py [-h] n order

benchmark the additive phylogeny algorithm

positional arguments:
  n           the maximum matrix size to benchmark the algorithm on
  order       a comma separated list of integer order polynomials to regress the runtime with

optional arguments:
  -h, --help  show this help message and exit
```
Example invocation: `python bench.py 30 "1,2,3"`
Warning: Large values of n (>100) can take a very long time!
