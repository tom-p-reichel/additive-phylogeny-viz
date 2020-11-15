import numpy as np
import itertools

def trimming_factor(d):
	"""
		find the trimming factor of a square distance matrix (numpy)
		return the trimming factor AND the degenerate triple it causes
	"""
	# get all i,j,k combinations
	i,j,k = np.array(list(itertools.permutations(range(d.shape[0]),3))).T

	# find the trimming factors required to make any triple a degenerate triple
	trimmingfactors = (d[i][j]+d[j][k]-d[i][k])/2

	# find the indexes where these factors are positive and filter to only those
	pindices = np.argwhere(trimmingfactors>0).flatten()
	i,j,k,trimmingfactors = i[pindices],j[pindices],k[pindices],trimmingfactors[pincides]

	# return the maximum
	m = np.argmax(trimmingfactors)

	return trimmingfactors[m],i[m],j[m],k[m]