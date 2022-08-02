""" Sampling from graphs """

__author__ = "Elisabetta Bergamini"

def bfsSample(G, source=None, k = 50):
	""" 
	bfsSample(G, source=None, k=50)    

	Start a BFS from source node, return node-induced subgraph of the first k nodes discovered.

	Parameters
	----------
	G : networkit.Graph
		The input graph.
	source : int, optional
		The starting node. If none is choosen, then a random node is picked. Default: None
	k : int, optional
		Stop after k nodes are discovered. Default: 50

	Returns
	-------
	networkit.Graph
		Subgraph based on bfsSample.
	"""
	if not source:
		source = nk.graphtools.randomNode(G)
	n = G.numberOfNodes()
	visited = [False]*n
	Q = [source]
	closest = {source}
	global found
	found = 0
	while Q and found < k:
		u = Q.pop(0)
		def enqueue(u,v,weight, eid):
			global found
			if not visited[v] and found < k:
				found += 1
				visited[v] = True
				Q.append(v)
				closest.add(v)
		G.forEdgesOf(u, enqueue)
	print("found {0} nodes".format(len(closest)))
	G1 = nk.graphtools.subgraphFromNodes(G, closest)
	return G1
