# distutils: language=c++

from networkit.exceptions import ReducedFunctionalityWarning
from libc.stdint cimport uint64_t
from libcpp.vector cimport vector

ctypedef uint64_t count
ctypedef uint64_t index
ctypedef index node

from .base cimport _Algorithm, Algorithm
from .graph cimport _Graph, Graph

import warnings
try:
	import pandas
except:
	warnings.warn("WARNING: module 'pandas' not found, some functionality will be restricted", ReducedFunctionalityWarning)

cdef extern from "<networkit/Globals.hpp>" namespace "NetworKit":

	index _none "NetworKit::none"

none = _none

cdef extern from "<networkit/simulation/EpidemicSimulationSEIR.hpp>":

	cdef cppclass _EpidemicSimulationSEIR "NetworKit::EpidemicSimulationSEIR" (_Algorithm):
		_EpidemicSimulationSEIR(_Graph, count, double, count, count, node) except +
		vector[vector[count]] getData() except +

cdef class EpidemicSimulationSEIR(Algorithm):
	"""
	EpidemicSimulationSEIR(G, tMax, transP, eTime, iTime, zero)

	Simulates an epidemic spread using the Susceptible-Exposed-Infectious-Removed (SEIR) model.

 	Parameters
 	----------
 	G : networkit.Graph
 		The graph.
 	tMax : int
 		Maximum number of timesteps.
	transP : float
		Transmission probability.
	eTime : int
		Exposed time
	iTime : int
		Infectious time.
	zero : int
		Starting node.
	"""
	cdef Graph G
	def __cinit__(self, Graph G, count tMax, double transP=0.5, count eTime=2, count iTime=7, node zero=none):
		self.G = G
		self._this = new _EpidemicSimulationSEIR(G._this, tMax, transP, eTime, iTime, zero)

	def getData(self):
		"""
		getData

		Returns a pandas object, containing the simulation data Only valid after run() is called. 

		Returns
		-------
		pandas.DataFrame
			The simulation data.
		"""
		return pandas.DataFrame((<_EpidemicSimulationSEIR*>(self._this)).getData(), columns=["zero", "time", "state", "count"])



