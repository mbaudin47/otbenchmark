# -*- coding: utf-8 -*-
# Copyright 2020 EDF
"""
Test for AxialStressedBeamReliabilityBenchmarkProblem class.
"""
import otbenchmark as otb
import unittest
import numpy as np
import openturns as ot

class CheckAxialStressedBeamReliabilityBenchmarkProblem(unittest.TestCase):

    def test_AxialStressedBeamReliabilityBenchmarkProblem(self):
        problem = otb.AxialStressedBeamReliabilityBenchmarkProblem()
        pf = problem.getProbability()
        print("pf=", pf)
        pf_exacte = 0.029198194624830955
        np.testing.assert_allclose(pf, pf_exacte, rtol=1.e-15)

    def test_UseCase(self):
        problem = otb.AxialStressedBeamReliabilityBenchmarkProblem()
        event = problem.getEvent()
        
        # Create a Monte Carlo algorithm
        experiment = ot.MonteCarloExperiment()
        algo = ot.ProbabilitySimulationAlgorithm(event, experiment)
        algo.setMaximumCoefficientOfVariation(0.05)
        algo.setMaximumOuterSampling(int(1e5))
        algo.run()
        
        # Retrieve results
        result = algo.getResult()
        computed_pf = result.getProbabilityEstimate()
        exact_pf = problem.getProbability()
        print('exact_pf=', exact_pf )
        print('computed_pf=', computed_pf )
        samplesize = result.getOuterSampling() * result.getBlockSize()
        print("Sample size : ", samplesize)
        atol = 1.0 / np.sqrt(samplesize)
        np.testing.assert_allclose(computed_pf, exact_pf, atol=atol)
            
if __name__=="__main__":
    unittest.main()
