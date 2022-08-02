""" This module deals with the conversion of graphs into matrices and linear algebra operations on graphs """


__author__ = "Christian Staudt"

# local imports

# external imports
import scipy.sparse
from scipy.sparse import csgraph, linalg
import numpy as np

def column(matrix, i):
	""" 
	column(matrix, i)

	Get the ith column of a matrix

	Parameters
	----------
	matrix : sparse matrix
		The matrix to compute the eigenvectors of
	i : int
		column index

	Returns
	-------
	list
		column i of matrix
	"""	
	return [row[i] for row in matrix]


def adjacencyMatrix(G, matrixType="sparse"):
	""" 
	adjacencyMatrix(G, matrixType="sparse")

	Get the adjacency matrix of the graph `G`.

	Parameters
	----------
	G : networkit.Graph
		The graph.
	matrixType : string
		either "sparse" or "dense"

	Returns
	-------
	:py:class:`scipy.sparse.csr_matrix`
		The adjacency matrix of the graph.
	"""
	n = G.upperNodeIdBound()
	if matrixType == "sparse":
		A = scipy.sparse.lil_matrix((n,n))
	elif matrixType == "dense":
		A = np.zeros(shape=(n,n))
	else:
		raise InputError("unknown matrix type: '{0}'".format(matrixType))
	# TODO: replace .edges() with efficient iterations
	if G.isWeighted():
		if G.isDirected():
			def processEdge(u,v,w,id):
				A[u, v] = w
		else:
			def processEdge(u,v,w,id):
				A[u, v] = w
				A[v, u] = w
	else:
		if G.isDirected():
			def processEdge(u,v,w,id):
				A[u, v] = 1
		else:
			def processEdge(u,v,w,id):
				A[u, v] = 1
				A[v, u] = 1
	G.forEdges(processEdge)
	if matrixType == "sparse":
		A = A.tocsr()  # convert to CSR for more efficient arithmetic operations
	return A

def laplacianMatrix(G):
	""" 
	laplacianMatrix(G)

	Get the laplacian matrix of the graph `G`.

	Parameters
	----------
	G : networkit.Graph
		The graph.

	Returns
	-------
	ndarray
		The N x N laplacian matrix of graph.
	ndarray
		The length-N diagonal of the laplacian matrix.
		diag is returned only if return_diag is True.
	"""
	A = adjacencyMatrix(G)
	return scipy.sparse.csgraph.laplacian(A)

def PageRankMatrix(G, damp=0.85):
	"""
	PageRankMatrix(G, damp=0.85)

	Builds the PageRank matrix of the undirected Graph `G`. This matrix corresponds with the
	PageRank matrix used in the C++ backend.


	Parameters
	----------
	G : networkit.Graph
		The graph.
	damp: float, optional
		Damping factor of the PageRank algorithm (0.85 by default)

	Returns
	-------
	ndarray
		The N x N page rank matrix of graph.
	"""
	A = adjacencyMatrix(G)

	n = G.numberOfNodes()
	stochastify = scipy.sparse.lil_matrix((n,n))
	for v in G.iterNodes():
		neighbors = G.degree(v)
		stochastify[v,v] = 0.0 if neighbors == 0 else 1.0 / neighbors
	stochastify = stochastify.tocsr()

	stochastic = A * stochastify

	dampened = stochastic * damp

	teleport = scipy.sparse.identity(G.numberOfNodes(), format="csr") * ((1 - damp) / G.numberOfNodes())

	return dampened + teleport

def symmetricEigenvectors(matrix, cutoff=-1, reverse=False):
	"""
	symmetricEigenvectors(matrix, cutoff=-1, reverse=False)

	Computes eigenvectors and -values of symmetric matrices.

	Parameters
	----------
	matrix : sparse matrix
		The matrix to compute the eigenvectors of
	cutoff : int, optional
		The maximum (or minimum) magnitude of the eigenvectors needed
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( [ float ], [ ndarray ] )
		A tuple of ordered lists, the first containing the eigenvalues in descending (ascending) magnitude, the
		second one holding the corresponding eigenvectors.

	"""
	if cutoff == -1:
		cutoff = matrix.shape[0] - 3

	mode = "SA" if reverse else "LA"
	w, v = scipy.sparse.linalg.eigsh(matrix, cutoff + 1, which=mode)

	orderlist = zip(w, range(len(w)))
	orderlist = sorted(orderlist)

	orderedW = column(orderlist, 0)
	orderedV = [v[:,i] for i in column(orderlist, 1)]

	return (orderedW, orderedV)

def eigenvectors(matrix, cutoff=-1, reverse=False):
	"""
	eigenvectors(matrix, cutoff=-1, reverse=False)

	Computes eigenvectors and -values of matrices.

	Parameters
	----------
	matrix : sparse matrix
		The matrix to compute the eigenvectors of
	cutoff : int, optional
		The maximum (or minimum) number of eigenvectors needed
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( [ float ], [ ndarray ] )
		A tuple of ordered lists, the first containing the eigenvalues in descending (ascending) magnitude, the
		second one holding the corresponding eigenvectors

	"""
	if cutoff == -1:
		cutoff = matrix.shape[0] - 3

	mode = "SR" if reverse else "LR"
	w, v = scipy.sparse.linalg.eigs(matrix, cutoff + 1, which=mode)

	orderlist = zip(w, range(len(w)))
	orderlist = sorted(orderlist)

	orderedW = column(orderlist, 0)
	orderedV = [v[:,i] for i in column(orderlist, 1)]

	return (orderedW, orderedV)

def laplacianEigenvectors(G, cutoff=-1, reverse=False):
	"""
	laplacianEigenvectors(G, cutoff=-1, reverse=False)

	Computes eigenvectors and -values of the Laplician matrix of G.

	Parameters
	----------
	G : networkit.graph
		The graph.
	cutoff : int, optional
		The maximum (or minimum) number of eigenvectors needed
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( [ float ], [ ndarray ] )
		 A tuple of ordered lists, the first containing the eigenvalues in descending (ascending) magnitude, the
		 second one holding the corresponding eigenvectors

	"""
	if G.isDirected():
		return eigenvectors(laplacianMatrix(G), cutoff=cutoff, reverse=reverse)
	else:
		return symmetricEigenvectors(laplacianMatrix(G), cutoff=cutoff, reverse=reverse)

def adjacencyEigenvectors(G, cutoff=-1, reverse=False):
	"""
	adjacencyEigenvectors(G, cutoff=-1, reverse=False)

	Computes eigenvectors and -values of the Adjacency matrix of G.

	Parameters
	----------
	G : networkit.graph
		The graph.
	cutoff : int, optional
		The maximum (or minimum) number of eigenvectors needed
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( [ float ], [ ndarray ] )
		A tuple of ordered lists, the first containing the eigenvalues in descending (ascending) magnitude, the
		second one holding the corresponding eigenvectors

	"""
	if G.isDirected():
		return eigenvectors(adjacencyMatrix(G), cutoff=cutoff, reverse=reverse)
	else:
		return symmetricEigenvectors(adjacencyMatrix(G), cutoff=cutoff, reverse=reverse)

def laplacianEigenvector(G, i, reverse=False):
	"""
	laplacianEigenvector(G, i, reverse=False)

	Compute a certain eigenvector and -value of the Laplician matrix of G.

	Parameters
	----------
	G : networkit.graph
		The graph.
	i : int
		Computes the eigenvector and value of index i 
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( float, ndarray )
		 A pair of values, the first containing the eigenvalue, the
		 second one holding the corresponding eigenvector

	"""
	if G.isDirected():
		spectrum = eigenvectors(laplacianMatrix(G), cutoff=i, reverse=reverse)
	else:
		spectrum = symmetricEigenvectors(laplacianMatrix(G), cutoff=i, reverse=reverse)

	return (spectrum[0][i], spectrum[1][i])

def adjacencyEigenvector(G, i, reverse=False):
	"""
	adjacencyEigenvector(G, i, reverse=False)

	Compute a certain eigenvector and eigenvalue of the Adjacency matrix of G.

	Parameters
	----------
	G : networkit.graph
		The graph.
	i : int
		Computes the eigenvector and value of index i 
	reverse : boolean, optional
		If set to true, the smaller eigenvalues will be computed before the larger ones

	Returns
	-------
	( float, ndarray )
		 A pair of values, the first containing the eigenvalue, the
		 second one holding the corresponding eigenvector

	"""
	if G.isDirected():
		spectrum = eigenvectors(adjacencyMatrix(G), cutoff=i, reverse=reverse)
	else:
		spectrum = symmetricEigenvectors(adjacencyMatrix(G), cutoff=i, reverse=reverse)

	return (spectrum[0][i], spectrum[1][i])
