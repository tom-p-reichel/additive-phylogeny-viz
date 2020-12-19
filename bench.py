from additive_phylogeny import *
from utilities import *
import argparse
import pickle
import numpy as np
import os
import time
import matplotlib.pyplot as plt




parser = argparse.ArgumentParser(description="benchmark the additive phylogeny algorithm")
parser.add_argument("n",help="the maximum matrix size to benchmark the algorithm on")
parser.add_argument("order",help="a comma separated list of integer order polynomials to regress the runtime with")
args = parser.parse_args()

n = int(args.n)
dat = np.zeros((n-2,2))
for x in range(2,n):
	print(x)
	for i in range(2):
		tree = createTree(x)
		d = getdistancematrix(tree,list(range(x)))
		st = time.time()
		bt = backtrace(*additive_phylogeny(d))
		ft = time.time()-st
		dat[x-2][i]=ft
#dat = pickle.load(open("tdata.pk","rb"))
dat = dat.mean(axis=1)


for p in args.order.split(","):
	p = int(p)+1
	regX = np.zeros((p,n-2))
	for x in range(p):
		print(x)
		regX[x,:] = np.arange(2,n)**x

	regX = regX.T

	# least squares regression for a polynomial of order p
	theta = np.linalg.inv(regX.T@regX)@regX.T@dat.reshape((dat.shape[0],1))

	plt.plot(regX@theta,label=f"least-squares polynomial of order {p-1}")

plt.plot(dat,label="true data")


plt.xlabel("n")
plt.xlabel("time (seconds)")
plt.title("additive phylogeny runtime")
plt.legend()
plt.show()
