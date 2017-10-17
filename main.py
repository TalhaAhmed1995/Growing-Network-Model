import numpy as np
from matplotlib import pyplot as plt
import random
import timeit

import ba
import analysis as ans
import plotting as pt


start = timeit.default_timer()

multiM = False # For varying m with fixed N
multiN = True # For varying N with fixed m
random = False # Make this true if running Phase 2
walk = False # Make this true if running Phase 3

if multiM: # For varying m with fixed N
    N = 10000 # Speciying the fixed N value to use
    mMinPower = 3 # The lowest power of 2 for m
    mMaxPower = 8 # The highest power of 2 for m

elif multiN: # For varying N with fixed m
    m = 3 # Speciying the fixed m value to use
    NminPower = 2 # The lowest power of 10 for N
    NmaxPower = 5 # The highest power of 10 for N

### PLEASE KEEP THE NUMBER OF LOOPS BELOW 3 FOR QUICK TESTING OF THE CODE, AS IT CAN TAKE A LONG TIME TO RUN FOR LARGER VALUES ###
loops = 1 # The total number of times the simulations are looped to improve statistics.

L = 6 # Specifying the length of the random walk
a=1.2 # Log binning bin width factor

multiGraphs = [] # Storing the graphs from all the simulations
multiGraphsData = [] # Storing the data for all the graphs, including degrees, nodes and edges
multiGraphsDegrees = [] # Storing the degrees from the graphs from all the simulations

def simulateModel(graphs, random=False, walk=False):
    """ Simulates the model by appeneding a new node with m edges per iteration"""

    graphsData = []
    time = [0] # Recording the time

    for graph in graphs: # Iterating over all graph objects
        n0 = graph.getn0()
        N = graph.getN()
        tMax = N - n0 # Finding the max number of iterations required to reach N nodes
        for i in range(1, tMax+1):
            if graphs.index(graph) == 0:
                time.append(i) # Storing t values
            graph.newNode(n0+i-1) # Appeneding a new node
            if walk and not random:
                graph.addWalkConnections() # Adding edges via Phase 1
            elif random and not walk:
                graph.addRandomConnections() # Adding edges via Phase 2
            else:
                graph.addConnections() # Adding edges via Phase 3

        graph.addNewNodes() # Compiling all the new nodes via networkx
        graph.addNewEdges() # Compiling all the new edges via networkx

        ### Collecting all the data required for analysis ###
        nodes = graph.getNodes()
        edges = graph.getEdges()
        degrees = graph.getDegrees()
        degreeValues = graph.getDegrees(values=True, sort=True)
        finalData = [nodes, edges, degrees, degreeValues]
        graphsData.append(finalData)

    time = np.asarray(time, dtype='int64')

    return time, graphsData # Returning the time and graph data

### SIMULATING THE MODEL FOR ALL SYSTEM SIZES USING THE SPECIFIED PARAMETERS ###
for i in range(loops):
    print i + 1 # Printing the current loop value
    if multiM: # For varying m with fixed N
        graphs = [ba.BA(2**x, N, L) for x in range(int(mMinPower), int(mMaxPower)+1)] # Instantiating graph objects with different m
    elif multiN: # For varying N with fixed m
        graphs = [ba.BA(m, 10**y, L) for y in range(int(NminPower), int(NmaxPower)+1)] # Instantiating graph objects with different N

    multiGraphs.append(graphs)

    time, graphsData = simulateModel(graphs=graphs, random=random, walk=walk) # Simulating the model with the graph objects created

    graphsDegrees = [] # Getting the degree distributions from each graph
    for data in graphsData:
        degrees = data[3]
        degrees = np.asarray(degrees, dtype='int64')
        graphsDegrees.append(degrees)

    multiGraphsData.append(graphsData)
    multiGraphsDegrees.append(graphsDegrees)

analysis = ans.Analysis(graphs=multiGraphs, degrees=multiGraphsDegrees, a=a, random=random, loops=loops) # Creating an analysis object using the data collected
analysis.sortDegrees() # Compiling all the graph degrees in their corresponding locations from all the looped simulations

### Computing and plotting the raw and theoretical probs ###
if multiM:
    K, KProbs, KCounts, expectedCounts, graphsCentres, graphsProbs, theoryData = analysis.degreeProb(raw=True, binned=True, pRaw=True, pBinned=True, plotTheory=False, plotRatio=False, checkSum=True, plot=True, log=True)
    K, KProbs, KCounts, expectedCounts, graphsCentres, graphsProbs, theoryData = analysis.degreeProb(raw=True, binned=True, pRaw=False, pBinned=True, plotTheory=True, plotRatio=False, checkSum=False, plot=True, log=True)
elif multiN:
    K, KProbs, KCounts, expectedCounts, graphsCentres, graphsProbs, theoryData = analysis.degreeProb(raw=True, binned=True, pRaw=False, pBinned=True, plotTheory=False, plotRatio=False, checkSum=False, plot=True, log=True)
if not walk:
    analysis.chiTest(counts=KCounts, expected=expectedCounts, removeFatTail=False, showCounts=False) # Performing a chi squared test with the fat tail
    analysis.chiTest(counts=KCounts, expected=expectedCounts, removeFatTail=True) # Performing a chi squared test without the fat tail
    if multiN:
        analysis.dataCollapse(graphCentres=graphsCentres, graphProbs=graphsProbs, plotType='o-', log=True) # Data collapsing
        analysis.plotK1(plotRatio=True, log=True, logRatio=True) # Plotting k1 against N

# print "Degrees for m = " +str(multiGraphs[0][0].getM()) + ": ", np.sort(multiGraphsDegrees[0][0]) # Prinitng the degrees for the smallest m graph


stop = timeit.default_timer()
print stop - start

plt.show()
