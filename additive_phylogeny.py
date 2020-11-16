import numpy as np
import itertools

class TreeNode:
	def __init__(self,name,parent,distance,child1=None,child2=None):
		self.name=name
		self.parent=parent
		self.distance = distance
		self.a=child1
		self.b=child2

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
				  [5,0,8,7],
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
	pindices = np.argwhere(trimmingfactors>0).flatten()
	i,j,k,trimmingfactors = i[pindices],j[pindices],k[pindices],trimmingfactors[pindices]

	# return the minimum
	m = np.argmin(trimmingfactors)

	return trimmingfactors[m],i[m],j[m],k[m]

def additive_phylogeny(d):
	d = d.copy()
	factors = []
	removed = []
	remaining = list(range(d.shape[0]))
	while(d.shape[0]>2):
		print("next run")
		print(remaining)
		print(d)
		trimming,i,j,k = trimming_factor(d)
		# subtract the trimming factor everywhere but the diagonal
		d-=(1-np.identity(d.shape[0]))*(2*trimming)
		factors.append(trimming) # for backtrace
		removed.append((remaining[i],remaining[j],remaining[k]))
		remaining.remove(remaining[j])
		d = d[list(range(j))+list(range(j+1,d.shape[0]))]
		d = d.T[list(range(j))+list(range(j+1,d.shape[1]))].T
	# add last distance & last two attributes for backtrace...
	print("next run")
	print(remaining)
	print(d)
	factors = factors + [d[0][1]]
	removed = removed + [(remaining[0],remaining[1])]
	return factors,removed

print(additive_phylogeny(test1))
print(additive_phylogeny(test2))


# WORK IN PROGRESS
#              v distance between last two nodes
#              v                              v last two nodes
# ([1.0, 2.0, 2.0], [(2, 0, 1), (1, 3, 2), (1, 2)])
def backtrace(factors, removed): 
	# factors[-1] = last distance between last two nodes left in add_phyl
	# removed[-1] = tuple of only two nodes
	temp_tuple = removed.pop(-1)
	a = TreeNode(temp_tuple[0], None, factors[-1])
	b = TreeNode(temp_tuple[1], a, factors[-1])
	a.parent = b
	
	# (self,name,parent,distance,child1=None,child2=None)
	# node_tuple is (i, j, k), when j was removed 
	for node_tuple in removed: 
		# IDEA: 
		# 	make j 
		#	make new internal node w j as parent
		# 	dist from j to internal node was the trimmed factor
		#	make i and k be children of new internal node
		# 	set internal node as parent of i and k
		# 	set distances i and k to be dist += trimming factor
		# 		then on next recursion: 
		# 		new j node
		# 		new internal node ***how to find distance? 
		# j = TreeNode(node_tuple, None, ???, )

		# v = TreeNode(???, None, ???, a, b)
		pass
