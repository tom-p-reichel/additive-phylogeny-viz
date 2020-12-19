from additive_phylogeny import *
from utilities import *
import argparse
import pickle
import numpy as np
import os
import time
import matplotlib.pyplot as plt

n = 50
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


for p in range(3,5):
	regX = np.zeros((p,n-2))
	for x in range(p):
		print(x)
		regX[x,:] = np.arange(2,n)**x

	regX = regX.T

	# least squares regression for a polynomial of order p
	theta = np.linalg.inv(regX.T@regX)@regX.T@dat.reshape((dat.shape[0],1))

	plt.plot(regX@theta,label=f"least-squares polynomial of order {p-1}")

plt.plot(dat,label="true data")

plt.legend()
plt.show()
