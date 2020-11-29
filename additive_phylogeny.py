import numpy as np
import itertools
from utilities import *
import os

test1 = np.array([[0,5,3,4],
				  [5,0,6,3],
				  [3,6,0,5],
				  [4,3,5,0]
				],dtype="float32")
# """
# A      B
# 1\_2__/ 2
# 2/    \ 1
# C      D
# """

# test2... i think?
# """
# A      B
# 1\_2__/ 4
# 2/    \ 3
# C      D
# """

# """
#        B(1)
#   _3__/ 3
#  /    \ 2
# C(2)   D(3)
# """

# """
#        B(1)
#   _2__/ 
#  /    
# C(2)   
# """


test2 = np.array([[0,7,3,6],
				  [7,0,8,7],
				  [3,8,0,7],
				  [6,7,7,0]
				],dtype="float32")


def trimming_factor(d):
	"""
		find the trimming factor of a square distance matrix (numpy)
		return the trimming factor AND the degenerate triple it causes
	"""
	# get all i,j,k combinations
	i,j,k = np.array(list(itertools.permutations(range(d.shape[0]),3))).T

	# find the trimming factors required to make any triple a degenerate triple
	trimmingfactors = (d[i,j]+d[j,k]-d[i,k])/2

	# find the indexes where these factors are positive and filter to only those
	pindices = np.argwhere(trimmingfactors>=0).flatten()
	i,j,k,trimmingfactors = i[pindices],j[pindices],k[pindices],trimmingfactors[pindices]

	# return the minimum
	m = np.argmin(trimmingfactors)

	return trimmingfactors[m],i[m],j[m],k[m]

def add_trimming_factor(t, trimming):
	# find every leaf and add trimming parameter 
	# check format in roots
	roots = getroots(t)
	add_trimming_factor_helper(roots[0],trimming)
	add_trimming_factor_helper(roots[1],trimming)

def add_trimming_factor_helper(t,trimming):
	#print(t,t.child1,t.child2)
	# SPECIAL CASE
	if (t is None):
		return
	if (t.child1 is t.child2 and t.child2 is None):
		# add trimming factor
		t.distance += trimming
		if (t.parent.parent is t): # special case
			t.parent.distance += trimming
		return
	else:
		add_trimming_factor_helper(t.child1,trimming)
		add_trimming_factor_helper(t.child2,trimming)


def additive_phylogeny2(d):
	d = d.copy()
	factors = []
	ds = []
	removed = []
	remaining = list(range(d.shape[0]))
	while(d.shape[0]>2):
		"""
		print("next run")
		print(remaining)
		print(d)
		"""
		trimming,i,j,k = trimming_factor(d)
		# subtract the trimming factor everywhere but the diagonal
		d-=(1-np.identity(d.shape[0]))*(2*trimming)
		ds.append((remaining.copy(),d))
		factors.append(trimming) # for backtrace
		removed.append((remaining[i],remaining[j],remaining[k]))
		remaining.remove(remaining[j])
		d = d[list(range(j))+list(range(j+1,d.shape[0]))]
		d = d.T[list(range(j))+list(range(j+1,d.shape[1]))].T
	# add last distance & last two attributes for backtrace...
	"""
	print("next run")
	print(remaining)
	print(d)
	"""
	factors = factors + [d[0][1]]
	removed = removed + [(remaining[0],remaining[1])]
	ds.append((remaining,d))
	return factors,removed,ds

# nodes is only of leaf nodes
def getdistancematrix(r,nodes):
	d = np.zeros((len(nodes),len(nodes)))
	for c in itertools.combinations(nodes,2):
		dist = sum(treepath(getnodefromname(r,c[0]),c[1])[1::2])
		d[nodes.index(c[0]),nodes.index(c[1])]=dist
		d[nodes.index(c[1]),nodes.index(c[0])]=dist
	return d

def backtrace2(factors,removed,ds):
	# base case
	root1 = TreeNode(ds[-1][0][0],None,ds[-1][1][0,1],None,None)
	root2 = TreeNode(ds[-1][0][1],root1,ds[-1][1][0,1],None,None)
	root1.parent=root2
	print(ds[-1][0])
	print(getdistancematrix(root1,ds[-1][0]))
	print(ds[-1][1])
	for x in range(len(factors)-2,-1,-1):
		header,d = ds[x]
		i,j,k = removed[x]
		# go on, add the thing to the tree. i DARE you.
		path = treepath(getnodefromname(root1,i),k)
		acc = 0
		it = iter(enumerate(path[1::2]))
		goal_dist = d[header.index(i),header.index(j)]
		index = 0
		while acc<d[header.index(i),header.index(j)]:
			# print("acc: " + str(acc))
			# print("goal distance: " + str(goal_dist))
			index,tmp = next(it)
			acc+=tmp
		left,right = path[::2][index],path[::2][index+1]
		# get distance between left and where j is to be inserted
		dij = d[header.index(i),header.index(j)] - sum(treepath(left,i)[1::2])
		# insert the thing between left and right
		insertbetween(dij,left,TreeNode(j,None,None),right)
		# now we add the trimming factor
		print(factors[x])
		print(dij)
		print("debug distance matrixes:")
		print(header)
		print(getdistancematrix(root1,header))
		print(d)
		print(printtree(root1))
		add_trimming_factor(root1,factors[x])
	return root1

factors,rem,ds = additive_phylogeny2(test1)
print("forward run over")
print(factors)
print(rem)
print(ds)
print(printtree(backtrace2(factors,rem,ds)))

if (__name__=="__main__"):
	factors,rem,ds = additive_phylogeny2(test1)
	tree1 = backtrace2(factors,rem,ds)
	assert((getdistancematrix(tree1,[0,1,2,3])==test1).all())
	factors,rem,ds = additive_phylogeny2(test2)
	tree2 = backtrace2(factors,rem,ds)
	assert((getdistancematrix(tree2,[0,1,2,3])==test2).all())
	print(printtree(tree2))

	leaves = 20
	for x in range(1000):
		ttree = createTree(leaves)
		print("correct tree")
		print(printtree(ttree))
		d = getdistancematrix(ttree,list(range(leaves)))
		factors,rem,ds = additive_phylogeny2(d)
		tree = backtrace2(factors,rem,ds)
		print("output tree")
		print(printtree(tree))
		d2 = getdistancematrix(tree,list(range(leaves)))
		assert((d==d2).all())