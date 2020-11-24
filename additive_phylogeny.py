import numpy as np
import itertools
from utilities import *

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

def add_trimming_factor(t, trimming):
	# find every leaf and add trimming parameter 
	# check format in roots
	roots = getroots(t)
	for root in roots:
		current = root  
    	stack = [] # initialize stack
      
    	while True: 
        	if current is not None: 
              
            	stack.append(current) 
          
            	current = current.child1  
  
        	elif(stack): 
            	current = stack.pop()
            	current = current.child2
				if !current.child1 and !current.child2:
					# trimming changes for each node, need to get it
					# from where it's stored
					node.distance = trimming  
        	else: 
            	break
	
	

def additive_phylogeny(d):
	d = d.copy()
	factors = []
	d_ij = [] 
	removed = []
	remaining = list(range(d.shape[0]))
	while(d.shape[0]>2):
		print("next run")
		print(remaining)
		print(d)
		trimming,i,j,k = trimming_factor(d)
		d_ij.append(d[i,j]) # for backtrace and constructing tree
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
	return factors,removed,d_ij

print(additive_phylogeny(test1))
print(additive_phylogeny(test2))

# WORK IN PROGRESS
#              v distance between last two nodes
#              v                              v last two nodes 
#			   v                              v		 v d_ij
# ([1.0, 2.0, 2.0], [(2, 0, 1), (1, 3, 2), (1, 2)], [3.0, 5.0])
def backtrace(d, factors, removed, d_ij): 
	# factors[-1] = last distance between last two nodes left in add_phyl
	# removed[-1] = tuple of only two nodes
	temp_tuple = removed.pop(-1)
	a = TreeNode(temp_tuple[0], None, factors[-1])
	b = TreeNode(temp_tuple[1], a, factors[-1])
	a.parent = b 

	# (self,name,parent,distance,child1=None,child2=None)
	# node_tuple is (i, j, k), when j was removed 
	for i, node_tuple in reversed(list(enumerate(removed))): 
		# 11/18 Workspace:
			# get j
			# get d_ij
			# get trimming factor
			# get distance between i and k -> how to do this???
			# 	if i = k's parent or k = i's parent
			# 		then get i.distance or k.distance
			# 	if node(s) in between i and k
			# 		then must bidirectionally walk tree to find shared node
			# 		and sum up distances travelled
			# make new internal node
			# 	dist i to new internal node = x = d_ij - 2*trimming
			# 	dist j to new internal node = trimming
			# 	dist k to new internal node = d_ik - x

		i_name = node_tuple[0]
		i = getnodefromname(a_node,i)
		j_name = node_tuple[1]
		j = getnodefromname(a_node,j)
		k_name = node_tuple[2]
		k = getnodefromname(a_node,k)
		d = d_ij[i]
		trimming = factors[i]
		path_ik = treepath(i_node,k)

		# Find i and k as two connected nodes whose edge will be the edge j attaches to 
		# trace path starting from i
		# 	k = first node in which d_ij < d_i>pathnode
		# 	i = node immediately before on path

		i_node = path[0]
		k_node = path[1]
		for node in path_ik: 
			if 

		# insertbetween = (d,???j,???)



		# v = TreeNode(???, None, ???, a, b)
		pass