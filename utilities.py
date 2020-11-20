
class TreeNode:
	def __init__(self,name,parent,distance,child1=None,child2=None):
		self.name=name
		self.parent=parent
		self.distance=distance #distance to parent
		self.child1=child1
		self.child2=child2

def getroots(t):
	while (t.parent.parent!=t):
		t = t.parent
	return (t,t.parent)

def printtree(t):
	roots = getroots(t)
	acc = ["digraph {",f"node{id(roots[1])} -> node{id(roots[0])} [label=\"{roots[0].distance}\"];",f"node{id(roots[0])} -> node{id(roots[1])};"]
	printtree_helper(roots[0],acc)
	printtree_helper(roots[1],acc)
	acc.append("}")
	return "\n".join(acc)

def printtree_helper(t,acc):
    for x in [t.child1,t.child2]:
        if (not (x is None)):
            if (not (t.name is None)):
                acc.append(f"node{id(t)} [label=\"{t.name}\"];")
            acc.append(f"node{id(t)} -> node{id(x)} [label=\"{x.distance}\"];")
            printtree_helper(t.child1,acc)

def insertbetween(d,i,j,k):
	"""insert a node between two *directly connected nodes* """
	# i could be k's parent, k could be i's parent, or they could be each other's parents
	if (i.parent==k and not k.parent==i):
		return insertbetween(d,k,j,i) # symmetry
	# now we KNOW that k's parent is i.
	newbranch = TreeNode(None,i,d[i,j],k,j)
	assert(d[i,k]==k.distance) # sanity checking
	assert(d[i,j]<d[i,k])
	k.distance=k.distance-d[i,j]
	k.parent=newbranch
	if (i.parent==k):
		i.parent=newbranch
		i.distance=d[i,j]
	j.parent=newbranch
	j.distance=0
	if (i.child1==k):
		i.child1=newbranch
	if (i.child2==k):
		i.child2=newbranch


def treepath(root,b,path=[]):
    if (root.name==b):
        path.append(root.name)
        return path

    # Cases
    # If get to leaf not and is not b, return no path
    # If internal node, traverse all children first
    #	then move up to parent

    tmp = path.copy()
    pointers = [root.child1,root.child2,root.parent]
    for x in pointers: 
    	if x != None:
    		tmp = treepath(root,b,tmp)
    		if tmp: 
    			tmp.append(root)
    			return tmp

    # roots_tuple = getroots(start)
        
    # if root == start: 
    #     tmp = path.copy()
    #     tmp.append(root.name)
    #     tmp = treepath(start,root.parent,b,tmp)
    #     return tmp
    # else: 
    #     tmp = path.copy()
    #     tmp.append(root.name)
    #     child_path = None
    #     if root.child1 and (root.child1 != start): 
    #         tmp_return = treepath(start,root.child1,b,tmp)
    #         if tmp_return: 
    #             child_path = tmp_return
    #     if root.child2 and (root.child2 != start): 
    #         tmp_return = treepath(start,root.child2,b,tmp)
    #         if tmp_return: 
    #             child_path = tmp_return
    #     if child_path == None:
    #         # if we're going to go into a parent that's a get_root and we have seen it
    #         # if we're going to go into a parent that's a get_root and we haven't seent it
    #         if root.parent in roots_tuple: 
    #             if root.parent not in path: 
    #                 path = treepath(start,root.parent,b,tmp)
    #             else: 
    #                 # STOP RECURSING 
    #                 return None
    #         else: 
    #             path = treepath(start,root.parent,b,tmp)
    #     else: 
    #         path = child_path
        
    #     return path


def treepath_helper(root,b,path=[]):



if __name__=="__main__":
    # really small tree

    roota = TreeNode("roota",None,1,None,None)
    rootb = TreeNode("rootb",roota,1,None,None)
    roota.parent=rootb

    print(printtree(roota))

    # Example Tree of TreeNodes
    node7 = TreeNode(7,None,3,None,None)
    node8 = TreeNode(8,None,5,None,None)
    inner6 = TreeNode(6,None,1,node7,node8)
    node5 = TreeNode(5,None,4,None,None)
    node1 = TreeNode(1,None,2,None,None)
    node2 = TreeNode(2,None,2,None,None)
    inner3 = TreeNode(3,None,3,node1,node2)
    inner4 = TreeNode(4,inner6,1,inner3,node5)
    node7.parent = inner6
    node8.parent = inner6
    inner6.parent = inner4
    node5.parent = inner4
    inner3.parent = inner4
    node1.parent = inner3
    node2.parent = inner3
    print(printtree(node5))

    path = []
    print(treepath(node1,node1,node7,path))