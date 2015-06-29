/*
 * EigenvectorCentrality.cpp
 *
 *  Created on: 19.03.2014
 *      Author: Henning
 */

#include "EigenvectorCentrality.h"
#include "../auxiliary/NumericTools.h"

namespace NetworKit {

EigenvectorCentrality::EigenvectorCentrality(const Graph& G, double tol):
		Centrality(G, true), tol(tol)
{
	// do not execute algorithm on directed graphs since this is error prone
	// and can yield misleading results (wrong metric, not implementation fault!)
	if (G.isDirected()) {
		throw std::runtime_error("This algorithm does not work on directed graphs.");
	}
}

void EigenvectorCentrality::run() {
	count z = G.upperNodeIdBound();
	std::vector<double> values(z, 1.0);
	scoreData = values;

	double length = 0.0;
	double oldLength = 0.0;

	auto converged([&](double val, double other) {
		// compute residual
		return (Aux::NumericTools::equal(val, other, tol));
	});

	do {
		oldLength = length;

		// iterate matrix-vector product
		G.parallelForNodes([&](node u) {
			values[u] = 0.0;
			G.forNeighborsOf(u, [&](node v) {
				values[u] += G.weight(u, v) * scoreData[v];
			});
		});

//		// set everything very small to zero
//		G.parallelForNodes([&](node u) {
//			if (values[u] < 1e-16) {
//				values[u] = 0.0;
//			}
//		});

		// normalize values
		length = 0.0;
		length = G.parallelSumForNodes([&](node u) {
			return (values[u] * values[u]);
		});
		length = sqrt(length);

//		TRACE("length: ", length);
//		TRACE(values);

		assert(! Aux::NumericTools::equal(length, 1e-16));
		G.parallelForNodes([&](node u) {
			values[u] /= length;
		});

//		TRACE(values);

		scoreData = values;
	} while (! converged(length, oldLength));

	// check sign and correct if necessary
	if (scoreData[0] < 0) {
		G.parallelForNodes([&](node u) {
			scoreData[u] = fabs(scoreData[u]);
		});
	}

	hasRun = true;
}

} /* namespace NetworKit */
