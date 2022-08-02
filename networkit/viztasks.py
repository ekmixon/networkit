# local imports
from . import nxadapter
from . import community
from . import centrality
from .coarsening import ParallelPartitionCoarsening
from .support import MissingDependencyError

# external imports
try:
	import networkx
except ImportError:
	have_nx = False
else:
	have_nx = True

def save(name, dir="."):
	""" 
	save(name, dir=".")

	Save a figure.
	
	Parameters
	----------
	name : str
		Name of the output file.
	dir : str
		Output directory. Default: "."
	"""
	savefig(os.path.join(dir, "{0}.pdf".format(name)), bbox_inches="tight", transparent=True)


def coloringToColorList(G, coloring):
	"""
	coloringToColorList(G, coloring)

	Calculate node colors based on an input graph and color dict.

	Parameters
	----------
	G : networkit.Graph
		The input graph.
	coloring : dict()
		Coloring scheme as dict.

	Returns
	-------
	list(tuple(float, float, float))
		List with color values for each node.
	"""
	nColors = len(coloring.keys())

	return [float(coloring[v]) / nColors for v in G.iterNodes()]


def drawGraph(G, **kwargs):
	""" 
	drawGraph(G, **kwargs)
	
	Draws a graph via networkX. Passes additional arguments beyond the graph to networkx.draw(...).
	By default, node sizes are scaled between 30 and 300 by node degree.

	Parameters
	----------
	G : networkit.Graph
		The input graph.
	`**kwargs` : dict()
		Additional arguments for networkx.draw function.
	"""
	if not have_nx:
		raise MissingDependencyError("networkx")
	if not G.checkConsistency():
		print("WARNING: Multi-graph has been converted to simple graph for display")
		G.removeMultiEdges()
	nxG = nxadapter.nk2nx(G)
	if "node_size" not in kwargs:
		kwargs["node_size"] = [30+270*s for s in centrality.DegreeCentrality(G,True).run().scores()]
	networkx.draw(nxG, **kwargs)

def drawCommunityGraph(G, zeta, **kwargs):
	""" 
	drawCommunityGraph(G, zeta, **kwargs)	

	Draws the community graph for a given graph and partition. Passes any additional arguments to networkx.draw(...).
	By default, node sizes are scaled between 30 and 500 by community size.

	Parameters
	----------
	G : networkit.Graph
		The input graph.
	zeta : networkit.Partition
		The input partition.
	`**kwargs` : dict()
		Additional arguments for networkx.draw function.	
	"""
	if not have_nx:
		raise MissingDependencyError("networkx")
	cg = ParallelPartitionCoarsening(G,zeta)
	cg.run() # convert communities to nodes
	graph = cg.getCoarseGraph()
	comGraph = nxadapter.nk2nx(graph)
	if "node_size" not in kwargs:
		sizes = list(zeta.subsetSizeMap().values())
		max_size = max(sizes)
		sizes = [elem/max_size for elem in sizes]
		kwargs["node_size"] = [30+470*s for s in sizes]
	networkx.draw(comGraph, **kwargs)
