/*
 * EnsembleGTest.cpp
 *
 *  Created on: 31.12.2012
 *      Author: cls
 */

#include "EnsembleGTest.h"

namespace EnsembleClustering {

TEST_F(EnsembleGTest, testEnsembleClustererOnCliqueGraph) {

	EnsembleClusterer ensembleClusterer;
	// configure EnsembleClusterer
	QualityMeasure* qm = new Modularity();
	ensembleClusterer.setQualityMeasure(*qm);
	int b = 2; // number of base clusterers
	for (int i = 0; i < b; ++i) {
		Clusterer* baseClusterer = new LabelPropagation();
		ensembleClusterer.addBaseClusterer(*baseClusterer);
	}
	Clusterer* finalClusterer = new LabelPropagation();
	ensembleClusterer.setFinalClusterer(*finalClusterer);

	// generate clustered random graph with obvious community structure
	GraphGenerator graphGen;
	int64_t n = 42;
	int64_t k = 3;
	// these parameters generate a clique graph
	double pIn = 1.0;
	double pOut = 0.0;
	Graph G = graphGen.makeClusteredRandomGraph(n, k, pIn, pOut);

	// DEBUG
	GraphIO graphio;
	graphio.writeAdjacencyList(G, "sandbox/G_Clique.adjlist");
	// DEBUG


	Clustering zeta = ensembleClusterer.run(G);

	DEBUG("clustering produced by EnsembleClusterer: k=" << zeta.numberOfClusters()); zeta.print();

	// DEBUG
	if (zeta.numberOfNodes() != G.numberOfNodes()) {
		ERROR("clustering produced by EnsembleClusterer has " << zeta.numberOfNodes() << " entries but n = " << G.numberOfNodes());
	}
	// DEBUG

	EXPECT_TRUE(zeta.isProper(G)) << "the resulting partition should be a proper clustering";
	EXPECT_EQ(k, zeta.numberOfClusters()) << " " << k << " clusters (cliques) are easy to detect";

	Modularity modularity;
	double mod = modularity.getQuality(zeta, G);
	INFO("modularity produced by EnsembleClusterer: " << mod);

}


TEST_F(EnsembleGTest, testEnsembleClustererOnCliqueGraph_ManyBaseClusterers) {

	// generate clustered random graph with obvious community structure
	GraphGenerator graphGen;
	int64_t n = 1000;
	int64_t k = 10;
	// these parameters generate a clique graph
	double pIn = 1.0;
	double pOut = 0.0;
	Graph G = graphGen.makeClusteredRandomGraph(n, k, pIn, pOut);

	// DEBUG
	GraphIO graphio;
	graphio.writeAdjacencyList(G, "sandbox/G_Clique.adjlist");
	// DEBUG

	EnsembleClusterer ensembleClusterer;
	// configure EnsembleClusterer
	QualityMeasure* qm = new Modularity();
	ensembleClusterer.setQualityMeasure(*qm);
	int b = 10; // number of base clusterers
	for (int i = 0; i < b; ++i) {
		Clusterer* baseClusterer = new LabelPropagation();
		ensembleClusterer.addBaseClusterer(*baseClusterer);
	}
	Clusterer* finalClusterer = new LabelPropagation();
	ensembleClusterer.setFinalClusterer(*finalClusterer);



	Clustering zeta = ensembleClusterer.run(G);

	DEBUG("clustering produced by EnsembleClusterer: k=" << zeta.numberOfClusters()); zeta.print();

	// DEBUG
	if (zeta.numberOfNodes() != G.numberOfNodes()) {
		ERROR("clustering produced by EnsembleClusterer has " << zeta.numberOfNodes() << " entries but n = " << G.numberOfNodes());
	}
	// DEBUG

	EXPECT_TRUE(zeta.isProper(G)) << "the resulting partition should be a proper clustering";
	EXPECT_EQ(k, zeta.numberOfClusters()) << " " << k << " clusters (cliques) are easy to detect";

	Modularity modularity;
	double mod = modularity.getQuality(zeta, G);
	INFO("modularity produced by EnsembleClusterer: " << mod);

}


TEST_F(EnsembleGTest, testEnsembleClustererOnAlmostCliqueGraph) {

	EnsembleClusterer ensembleClusterer;
	// configure EnsembleClusterer
	QualityMeasure* qm = new Modularity();
	ensembleClusterer.setQualityMeasure(*qm);
	int b = 2; // number of base clusterers
	for (int i = 0; i < b; ++i) {
		Clusterer* baseClusterer = new LabelPropagation();
		ensembleClusterer.addBaseClusterer(*baseClusterer);
	}
	Clusterer* finalClusterer = new LabelPropagation();
	ensembleClusterer.setFinalClusterer(*finalClusterer);

	// generate clustered random graph with obvious community structure
	GraphGenerator graphGen;
	int64_t n = 20;
	int64_t k = 3;
	// these parameters generate a clique graph
	double pIn = 1.0;
	double pOut = 0.01;
	Graph G = graphGen.makeClusteredRandomGraph(n, k, pIn, pOut);

	// DEBUG
	GraphIO graphio;
	graphio.writeAdjacencyList(G, "sandbox/G_AlmostClique.adjlist");
	// DEBUG


	Clustering zeta = ensembleClusterer.run(G);

	DEBUG("clustering produced by EnsembleClusterer: k=" << zeta.numberOfClusters()); zeta.print();

	// DEBUG
	if (zeta.numberOfNodes() != G.numberOfNodes()) {
		ERROR("clustering produced by EnsembleClusterer has " << zeta.numberOfNodes() << " entries but n = " << G.numberOfNodes());
	}
	// DEBUG

	EXPECT_TRUE(zeta.isProper(G)) << "the resulting partition should be a proper clustering";
	EXPECT_EQ(k, zeta.numberOfClusters()) << " " << k << " clusters are easy to detect";

	Modularity modularity;
	double mod = modularity.getQuality(zeta, G);
	INFO("modularity produced by EnsembleClusterer: " << mod);

}





TEST_F(EnsembleGTest, testEnsembleClustererOnRandomGraph) {

	EnsembleClusterer ensembleClusterer;
	// configure EnsembleClusterer
	QualityMeasure* qm = new Modularity();
	ensembleClusterer.setQualityMeasure(*qm);
	int b = 2; // number of base clusterers
	for (int i = 0; i < b; ++i) {
		Clusterer* baseClusterer = new LabelPropagation();
		ensembleClusterer.addBaseClusterer(*baseClusterer);
	}
	Clusterer* finalClusterer = new LabelPropagation();
	ensembleClusterer.setFinalClusterer(*finalClusterer);

	GraphGenerator graphGen;
	int64_t n = 20;
	Graph G = graphGen.makeRandomGraph(20, 0.5);

	// DEBUG
	GraphIO graphio;
	graphio.writeAdjacencyList(G, "sandbox/G_Random.adjlist");
	// DEBUG


	Clustering zeta = ensembleClusterer.run(G);

	DEBUG("clustering produced by EnsembleClusterer: k=" << zeta.numberOfClusters()); zeta.print();

	// DEBUG
	if (zeta.numberOfNodes() != G.numberOfNodes()) {
		ERROR("clustering produced by EnsembleClusterer has " << zeta.numberOfNodes() << " entries but n = " << G.numberOfNodes());
	}
	// DEBUG

	EXPECT_TRUE(zeta.isProper(G)) << "the resulting partition should be a proper clustering";

	Modularity modularity;
	double mod = modularity.getQuality(zeta, G);
	INFO("modularity produced by EnsembleClusterer: " << mod);

}


TEST_F(EnsembleGTest, showPlantedClusteringDissimilarity) {

	EnsembleClusterer ensembleClusterer;
	// configure EnsembleClusterer
	QualityMeasure* qm = new Modularity();
	ensembleClusterer.setQualityMeasure(*qm);
	int b = 5; // number of base clusterers
	for (int i = 0; i < b; ++i) {
		Clusterer* baseClusterer = new LabelPropagation();
		ensembleClusterer.addBaseClusterer(*baseClusterer);
	}
	Clusterer* finalClusterer = new LabelPropagation();
	ensembleClusterer.setFinalClusterer(*finalClusterer);

	// make clustered random graph with planted partition
	int64_t n = 1000;	// number of nodes
	int k = 42; 			// number of clusters
	double pin = 0.5;
	double pout = 0.01;


	Graph none(n);		// dummy graph for clustering generation
	ClusteringGenerator clusteringGen;
	Clustering planted = clusteringGen.makeRandomClustering(none, k);

	GraphGenerator graphGen;
	Graph G = graphGen.makeClusteredRandomGraph(planted, pin, pout);

	Clustering found = ensembleClusterer.run(G);

	Modularity modularity;
	double mod = modularity.getQuality(found, G);


	JaccardMeasure jaccard;
	double j = jaccard.getDissimilarity(G, planted, found);

	RandMeasure rand;
	double r = rand.getDissimilarity(G, planted, found);

	INFO("EnsembleClusterer(LabelPropagation," << b << ") found " << found.numberOfClusters() << " of " << k << " clusters for (pin, pout) = (" << pin << ", " << pout << ")");
	INFO("Modularity of found clustering: " << mod);
	INFO("Jaccard dissimilarity between planted and found clustering: " << j);
	INFO("Rand dissimilarity between planted and found clustering: " << r);

	// TODO: what would it mean to fail the test?
	EXPECT_TRUE(found.isProper(G)) << "found clustering should be proper clustering of G";

}

} /* namespace EnsembleClustering */
