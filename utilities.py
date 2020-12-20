import random
from collections import defaultdict

class TreeNode:
    def __init__(self,name,parent,distance,child1=None,child2=None):
        self.name=name
        self.parent=parent
        self.distance=distance #distance to parent
        self.child1=child1
        self.child2=child2
    
    def __repr__(self):
        return f"node<{self.name}>"

def getroots(t):
    while (t.parent.parent!=t):
        t = t.parent
    return (t,t.parent)

def printtree(t,highlight=defaultdict(lambda:"black")):
    roots = getroots(t)
    acc = ["digraph {"] #,f"node{id(roots[0])} -> node{id(roots[1])} [label=\"{roots[0].distance}\"];",f"node{id(roots[0])} -> node{id(roots[1])};"]
    printtree_helper(roots[0],acc,highlight=highlight)
    printtree_helper(roots[1],acc,highlight=highlight)
    acc.append("}")
    return "\n".join(acc)

def printtree_helper(t,acc,highlight):
    if (not (t is None)):
        if (t.name is None):
            acc.append(f"node{id(t)} [label=\"\",color=\"{highlight[t]}\"];")
        else:
            acc.append(f"node{id(t)} [label=\"{t.name}\",color=\"{highlight[t]}\"];")
        acc.append(f"node{id(t.parent)} -> node{id(t)} [label=\"{t.distance}\"];")
        printtree_helper(t.child1,acc,highlight)
        printtree_helper(t.child2,acc,highlight)

def insertbetween(dij,i,j,k):
    """insert a node between two *directly connected nodes* """
    # i could be k's parent, k could be i's parent, or they could be each other's parents
    if (i.parent==k and not k.parent==i):
        return insertbetween(i.distance-dij,k,j,i) # symmetry
    # now we KNOW that k's parent is i.
    newbranch = TreeNode(None,i,dij,k,j)
    #assert(d[i.name,k.name]==k.distance) # sanity checking
    #assert(d[i.name,j.name]<d[i.name,k.name])
    k.distance=k.distance-dij
    k.parent=newbranch
    if (i.parent==k):
        i.parent=newbranch
        i.distance=dij
    j.parent=newbranch
    j.distance=0
    if (i.child1==k):
        i.child1=newbranch
    if (i.child2==k):
        i.child2=newbranch

# root == any node on the tree
# is a name
def getnodefromname(root,b):
    # TODO: this is an awful hack! too bad !
    return treepath(root,b)[-1]

def treepath(root,b,path=None):
    # ok so, putting a literal `[]` in the keyword argument actually preserves THAT list forever, so changes to it carry between function calls.
    # so we put a none in there, and create a brand new list.
    if (path is None): 
        path = []
    path.append(root)
    
    # print("treepath - appending root: " + str(root))

    # Base case if at leaf == b
    if (root.name==b):
        return path

    # Check children if any, return only if not None (means found b)
    tmp_path = path.copy()
    if root.child1:
        temp_path1 = treepath_helper(root.child1,b,tmp_path + [root.child1.distance]) 
        if temp_path1 != None: 
            return temp_path1
    if root.child2:
        temp_path2 = treepath_helper(root.child2,b,tmp_path + [root.child2.distance])
        if temp_path2 != None: 
            return temp_path2

    # Go up a parent
    roots = getroots(root)
    # print("roots: " + str(roots))
    # print("cur path: " + str(path))
    if roots[0] in path and roots[1] in path: 
        # print("returning bc both roots are in path already")
        return None
    path = treepath(root.parent,b,tmp_path + [root.distance])

    return path

def treepath_helper(root,b,path=[]):
    path = path + [root]
    #print(f"contemplating {root.name}")
    if (root.name==b):
        # base case
        return path
    if (not (root.child1 is None)):
        tmp = treepath_helper(root.child1,b,path=path + [root.child1.distance])
        if (not (tmp is None)):
            return tmp
    if (not (root.child2 is None)):
        tmp = treepath_helper(root.child2,b,path=path + [root.child2.distance])
        if (not (tmp is None)):
            return tmp
    return None

def createTree(numLeaves): 
    root_a = TreeNode("root_a",None,1,None,None)
    root_b = TreeNode("root_b",root_a,1,None,None)
    root_a.parent=root_b

    leaves = list(range(numLeaves))
    #print("leaves: " + str(leaves))
    random.shuffle(leaves)
    s = random.randint(1,len(leaves)-1)
    a,b = leaves[:s],leaves[s:]
    createTreeHelper(root_a, a)
    createTreeHelper(root_b, b)
    return root_a

def createTreeHelper(root, leaves):
    rand_dist1 = random.randint(1,10)
    rand_dist2 = random.randint(1,10)

    #print("(in helper) leaves: " + str(leaves))
    if len(leaves) <= 2: 
        for leaf in leaves: 
            rand_dist = random.randint(1,10)
            leaf = TreeNode(leaf, root, rand_dist, None, None)
            if root.child1 == None:
                root.child1 = leaf
            elif root.child2 == None:
                root.child2 = leaf
        return root
    # add leaves to given root

    random.shuffle(leaves)
    s = random.randint(1,len(leaves)-1)
    a,b = leaves[:s],leaves[s:]
    #print(a,b)

    # else split up leaves into two, create two new roots, recurse    

    roota = TreeNode(None, root, rand_dist1, None, None)
    rootb = TreeNode(None, root, rand_dist2, None, None)  
    root.child1 = roota
    root.child2 = rootb

    createTreeHelper(roota, a)
    createTreeHelper(rootb, b)

    return root


if __name__=="__main__":
    # really small tree

    roota = TreeNode("roota",None,1,None,None)
    rootb = TreeNode("rootb",roota,1,None,None)
    roota.parent=rootb
    print("trivial pathing case:")
    print(treepath(roota,rootb.name))
    
    print(printtree(roota))

    node7 = TreeNode(7,None,3,None,None)
    inner8 = TreeNode(8,None,5,None,None)
    inner6 = TreeNode(6,None,1,node7,inner8)
    node5 = TreeNode(5,None,4,None,None)
    node1 = TreeNode(1,None,2,None,None)
    node2 = TreeNode(2,None,2,None,None)
    inner3 = TreeNode(3,None,3,node1,node2)
    inner4 = TreeNode(4,inner6,1,inner3,node5)
    node7.parent = inner6
    inner8.parent = inner6
    inner6.parent = inner4
    node5.parent = inner4
    inner3.parent = inner4
    node1.parent = inner3
    node2.parent = inner3
    node9 = TreeNode(9,inner8,8,None,None)
    inner8.child1 = node9
    print(printtree(node5))

    path = []
    print("test btwn node1 and node2")
    print(treepath(node1,node2.name,path))
    path = []
    print("test btwn node1 and node5")
    print(treepath(node1,node5.name,path))
    path = []
    print("test btwn node 1 and node9")
    print(treepath(node1,node9.name,path))
