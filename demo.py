from additive_phylogeny import *
from utilities import *
import argparse
import h5py
import numpy as np
import os
import sys


def showtree(tree):
	dot = printtree(tree)
	with open("tmptree.dot","w") as f:
		f.write(dot)
	os.system("dot -Tpng tmptree.dot | feh -")


def savetree(tree,frame):
	dot = printtree(tree)
	with open("tmptree.dot","w") as f:
		f.write(dot)
	os.system(f"dot -Tpng tmptree.dot > {frame}")


p = argparse.ArgumentParser()
p.add_argument("--n",help="number of leaf nodes in randomly generated tree")
p.add_argument("--csv",help="a headerless csv file containing a distance matrix from which to generate an additive phylogeny")
p.add_argument("outputdir",help="a directory in which to place frames of the additive phylogeny algorithm")
args = p.parse_args()

if (args.n):
	n = int(args.n)
	tree = createTree(n)
	d = getdistancematrix(tree,list(range(n)))
elif (args.csv):
	with open(args.csv,"r") as f:
		d = np.array([[int(x) for x in l.split(",")] for l in f.readlines() if l!=""],dtype="float32")
else:
	sys.stderr.write("You need to provide at least one of `--n` or `--hd5` to provide a distance matrix to perform additive phylogeny on!\n")
	exit(0)

factors,rem,ds = additive_phylogeny(d)


for x in range(len(factors)):
	intermediate = backtrace(factors[-x:],rem[-x:],ds[-x:])
	savetree(intermediate,f"{args.outputdir}/{x}.png")
# os.cp(f"{args.outputdir}/0.png",f"{args.outputdir}/{len(factors)}.png")
# todo, make last frame same as frame 0
