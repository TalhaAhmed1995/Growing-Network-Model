import numpy as np
from scipy.optimize import curve_fit
from scipy import stats
from matplotlib import pyplot as plt
import random

import functions as funcs
import plotting as pt
import log_bin_CN_2016 as lb

class Analysis:

    def __init__(self, graphs, degrees, a, random, loops):

        self.graphs = graphs
        self.graphsDegrees = degrees
        self.a = a
        self.graphMs = np.array([graph.getM() for graph in self.graphs[0]], dtype='int64')
        self.graphNs = np.array([graph.getN() for graph in self.graphs[0]], dtype='int64')
        self.random = random
        self.sortedDegrees = []
        self.sortedK1s = []
        self.loops = float(loops)

    def sortDegrees(self):
        """ Compiles the degree distribution data from the various simulation runs into their corresponding arrays """

        for i in range(len(self.graphsDegrees[0])):
            combinedDegrees = [] # Accumulating the degree values for each m and N value
            k1Values = [] # Accumulating the k1 values
            for j in range(len(self.graphsDegrees)):
                degreesList = self.graphsDegrees[j][i]
                combinedDegrees.extend(degreesList)
                k1Values.append(degreesList[np.argmax(degreesList)])

            combinedDegrees = np.asarray(combinedDegrees, dtype='int64') # Converting to numpy arrays
            k1Values = np.asarray(k1Values, dtype='int64')
            combinedDegrees = np.sort(combinedDegrees)
            self.sortedDegrees.append(combinedDegrees)
            self.sortedK1s.append(k1Values)

        # print "Sorted Degrees Len: ", len(self.sortedDegrees)
        # print "Sorted K1s Len: ", len(self.sortedK1s)

    def degreeProb(self, raw=False, binned=False, pRaw=False, pBinned=False, plotTheory=False, plotRatio=False, checkSum=False, plot=False, plotType1='o', plotType2='o-', plotType3='-', log=False):
        """ Calculates the probabilities of getting degree values k, p(k) for all graphs. Also log-bins the data."""

        K = []
        KProbs = []
        KCounts = []
        expectedCounts = []
        graphsCentres = []
        graphsProbs = []
        theoryData = []

        if raw: # Raw probs calculated only is specified
            for i in range(len(self.sortedDegrees)):
                k = []
                probs = []
                averageCounts = []
                degrees = np.sort(self.sortedDegrees[i]) # Getting the list of degrees for the current graph size
                for x in degrees: # Going in ascending order of the degrees list
                    if x not in k:
                        k.append(x)
                        count = 0
                        for y in degrees:
                            if y == x:
                                count += 1 # Counting how many times the current degree value occurs in the list
                            elif count >= 1:
                                break # Since the list is sorted in ascending order, if the count is >= 1 and isn't increasing further, there are no more degrees with this value
                            else:
                                pass # If the degree value hasn't been found yet, keep scanning
                        if count == 0:
                            print "COUNT IS ZERO"
                        prob = count / float(len(degrees)) # Dividing the counted occurrences of all k values by the total number of degrees in the graph
                        averageCounts.append(count/self.loops) # Calculating the average counts number per degree by diving but the number of loops
                        probs.append(prob)
                    else:
                        pass
                k = np.asarray(k, dtype='int64') # Converting the lists to numpy arrays for easier manipulation
                averagecounts = np.asarray(averageCounts, dtype='float64')
                probs = np.asarray(probs, dtype='float64')
                K.append(k)
                KCounts.append(averageCounts)
                KProbs.append(probs)

                N = self.graphNs[i]
                if self.random:
                    theoryProbs = np.array([funcs.func2(float(k), float(self.graphMs[i])) for k in K[i]], dtype='float64')
                else:
                    theoryProbs = np.array([funcs.func1(float(k), float(self.graphMs[i])) for k in K[i]], dtype='float64')
                theoryCounts = N * theoryProbs # Calculating the theoretically expected degree counts
                expectedCounts.append(theoryCounts)

            # Converting the lists to numpy arrays for easier manipulation
            K = np.asarray(K)
            KCounts = np.asarray(KCounts)
            expectedCounts = np.asarray(expectedCounts)
            KProbs = np.asarray(KProbs)

            if checkSum: # Checking to see if all the probabilities add up to 1 ie they are normalised for all system sizes
                for probs in KProbs:
                    summation = np.sum(probs)
                    print "Summation: ", summation

        if binned: # Binned probs calculated only is specified
            for i in range(len(self.sortedDegrees)):
                degrees = self.sortedDegrees[i] # Getting the list of avalanche sizes for the current system size
                centres, binProbs = lb.log_bin(degrees, bin_start=float(self.graphMs[i]), a=self.a, datatype='integer') # Calculating the log-binned probs using the log_bin_CN_2016.py module
                graphsCentres.append(centres)
                graphsProbs.append(binProbs)

            for x in range(len(graphsCentres)): # Calculating the theoretical probability values
                if self.random:
                    theoryValues = np.array([funcs.func2(float(k), float(self.graphMs[x])) for k in graphsCentres[x]], dtype='float64')
                else:
                    theoryValues = np.array([funcs.func1(float(k), float(self.graphMs[x])) for k in graphsCentres[x]], dtype='float64')
                theoryData.append(theoryValues)

        if plot: # Plotting the probs p(k) against degree values k on log-log plots (if specified)
            xLab = r"$k$"
            title = "Degree Size Probability vs Degree Size"
            if pRaw and not pBinned: # Plotting just the raw data
                yLab = r"$p(k)$"
                legend = ['Raw for m = ' +str(i) for i in self.graphMs]
                if self.graphNs[0] != self.graphNs[-1]:
                    legend = ['Raw for N = ' +str(i) for i in self.graphNs]
                plotTypes = [plotType1 for i in range(len(KProbs))]
                pt.plot(xData=K, yData=KProbs, plotType=plotTypes, xLab=xLab, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log)
            elif pBinned and not pRaw: # Plotting just the binned data
                yLab = r"$\tildep(k)$"
                legend = ['Binned for m = ' +str(i) for i in self.graphMs]
                if self.graphNs[0] != self.graphNs[-1]:
                    legend = ['Binned for N = ' +str(i) for i in self.graphNs]
                plotTypes = [plotType1 for i in range(len(graphsProbs))]
                if plotTheory:
                    legend1 = ['Binned for m = ' +str(i) for i in self.graphMs]
                    legend2 = ['Theoretical for m = ' +str(i) for i in self.graphMs]
                    if self.graphNs[0] != self.graphNs[-1]:
                        legend1 = ['Binned for N = ' +str(i) for i in self.graphNs]
                        legend2 = ['Theoretical for N = ' +str(i) for i in self.graphNs]
                    plotTypes1 = [plotType1 for i in range(len(graphsProbs))]
                    plotTypes2 = [plotType3 for i in range(len(graphsProbs))]
                    plt.figure(figsize=(12, 10))
                    pt.plot(xData=graphsCentres, yData=graphsProbs, plotType=plotTypes1, xLab=xLab, yLab=yLab, title=title, legend=legend1, multiX=True, multiY=True, loc=1, log=log, figure=False)
                    pt.plot(xData=graphsCentres, yData=theoryData, plotType=plotTypes2, xLab=xLab, yLab=yLab, title=title, legend=legend2, multiX=True, multiY=True, loc=1, log=log, figure=False)
                    plt.grid()
                elif plotRatio: # Plotting the ratio of raw to theory probs
                    yLab = r"$p_{d}(k)/p_{t}(k)$"
                    legend = ['Binned for m = ' +str(i) for i in self.graphMs]
                    if self.graphNs[0] != self.graphNs[-1]:
                        legend = ['Binned for N = ' +str(i) for i in self.graphNs]
                    plotTypes = [plotType2 for i in range(len(graphsProbs))]
                    ratios = []
                    for i in range(len(graphsProbs)):
                        ratio = graphsProbs[i] / theoryData[i]
                        ratios.append(ratio)
                    plt.figure(figsize=(12, 10))
                    plt.axhline(y=1, linewidth=2, color = 'k')
                    pt.plot(xData=graphsCentres, yData=ratios, plotType=plotTypes, xLab=xLab, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log, figure=False)
                else:
                    legend = ['Binned for m = ' +str(i) for i in self.graphMs]
                    if self.graphNs[0] != self.graphNs[-1]:
                        legend = ['Binned for N = ' +str(i) for i in self.graphNs]
                    plotTypes = [plotType2 for i in range(len(graphsProbs))]
                    pt.plot(xData=graphsCentres, yData=graphsProbs, plotType=plotTypes, xLab=xLab, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log)

            elif pRaw and pBinned: # Plotting both the raw data and binned data
                yLab = r"$p(k)$"
                legend = ['Raw for m = ' +str(self.graphMs[-1]), 'Binned for m = ' +str(self.graphMs[-1])]
                plotTypes = [plotType1, plotType2]
                pt.plot(xData=[K[-1], graphsCentres[-1]], yData=[KProbs[-1], graphsProbs[-1]], plotType=plotTypes, xLab=xLab, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log)

        return K, KProbs, KCounts, expectedCounts, graphsCentres, graphsProbs, theoryData # Returning both the raw and binned data

    def chiTest(self, counts, expected, removeFatTail=False, showCounts=False):
        """ Performs a chi squared statistical test between the raw and theoretical results. Also gives the option of removing the fat tail """

        chiValues = []
        pValues = []

        for i in range(len(counts)):

            raw = counts[i]
            theoretical = expected[i]

            if showCounts: # Used for debugging
                print "Counts len:", len(raw)
                print "Expected len:", len(theoretical)
                print "Counts: ", raw
                print "Expected: ", theoretical
                print "Last raw value: ", raw[-1]
                print "Last theoretical value: ", theoretical[-1]

            if removeFatTail: # Removes the latter 15% of the data to reduce the effects of the fat tail
                raw = raw[:len(raw)-int(len(raw) * 0.15)]
                theoretical = theoretical[:len(theoretical)-int(len(theoretical) * 0.15)]

            chiSquare, p = stats.chisquare(raw, theoretical) # Performing the chi square test between the raw and theoretical data
            chiValues.append(chiSquare)
            pValues.append(p)

        chiValues = np.asarray(chiValues, dtype='float128') # Converting from lists to numpy arrays
        pValues = np.asarray(pValues, dtype='float128')

        # Printing the statistics calculated
        print "Fat Tail Removed? ", removeFatTail
        print "Chi Values: ", chiValues
        print "p Values: ", pValues

    def dataCollapse(self, graphCentres, graphProbs, plotType ='o-', log=False):
        """ Completely collapses the probabilities calculated by rescaling the vertical and horizontal axis """

        scaledGraphCentres = []
        scaledGraphCentres2 = []
        scaledGraphProbs = []

        for i in range(len(graphCentres)): # Calculating the reciprocal of the theoretical probs
            centres = graphCentres[i]
            probs = graphProbs[i]
            if self.random:
                factors = np.array([1./(funcs.func2(float(k), float(self.graphMs[i]))) for k in centres], dtype='float64')
            else:
                factors = np.array([1./(funcs.func1(float(k), float(self.graphMs[i]))) for k in centres], dtype='float64')

            m = float(self.graphMs[i])
            N = float(self.graphNs[i])
            if self.random: # Calculating the theoretical k1 value
                scaling = funcs.func4(N, m)
            else:
                scaling = funcs.func3(N, m)

            scaledCentres = centres / scaling # Scaling the horizontal axis as k / k1
            scaledProbs = probs * factors # Scaling the vertical axis as p_data / p_theory
            scaledGraphCentres.append(scaledCentres)
            scaledGraphProbs.append(scaledProbs)

        # Plotting the collapsed data
        xLab = r"$k / k_{1}$"
        xLab2 = r"$k$"
        yLab = r"$p_{data}(k) / p_{theory}(k)$"
        title = "Scaled Degree Size Probability vs Scaled Degree Size (DATA COLLAPSE)"
        legend = ['Scaled Binned for N = ' +str(i) for i in self.graphNs]
        plotTypes = [plotType for i in range(len(scaledProbs))]
        # Partially collapsing
        pt.plot(xData=graphCentres, yData=scaledGraphProbs, plotType=plotTypes, xLab=xLab2, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log)
        # Fully collapsing
        pt.plot(xData=scaledGraphCentres, yData=scaledGraphProbs, plotType=plotTypes, xLab=xLab, yLab=yLab, title=title, legend=legend, multiX=True, multiY=True, loc=1, log=log)

    def plotK1(self, plotRatio=False, plotType1='o', plotType2='-', plotType3='o-', log=False, logRatio=False):
        """ Calculates the average largest degree k1 for each graph and plots against N. Also calculates errors on k1 """

        m = float(self.graphMs[0])
        Nmin = float(self.graphNs[0])
        Nmax = float(self.graphNs[-1])
        Ns = np.linspace(Nmin, Nmax + 0.1, 1000)
        if self.random: # Extroplating the theoretical curve for k1
            theoryK1s = np.array([funcs.func4(N, m) for N in Ns], dtype='float64')
            theoryPoints = np.array([funcs.func4(N, m) for N in self.graphNs], dtype='float64')
        else:
            theoryK1s = np.array([funcs.func3(N, m) for N in Ns], dtype='float64')
            theoryPoints = np.array([funcs.func3(N, m) for N in self.graphNs], dtype='float64')

        rawK1s = np.array([np.mean(k1s) for k1s in self.sortedK1s], dtype='float64') # Calculating the average raw k1 values using a mean calculation
        rawK1Errors = np.array([np.std(k1s) for k1s in self.sortedK1s], dtype='float64') # Calculating the errors on the k1 values via STD

        ratios = theoryPoints / rawK1s # Calculating the ratio of the theoretical to raw k1 values

        # Printing the results obtained
        print "Theory K1s: ", theoryPoints
        print "Numerical K1s: ", rawK1s
        print "Ratios: ", ratios

        # Plotting k1 vs N
        xLab = r"$N$"
        yLab = r"$k_{1}$"
        title = "Highest Degree Node vs Network Size"
        legend1 = "Numerical k1 Values"
        legend2 = "Theoretical k1 Values"
        plt.figure(figsize=(12, 10))
        pt.plot(xData=self.graphNs, yData=rawK1s, plotType=plotType1, xLab=xLab, yLab=yLab, title=title, legend=legend1, loc=1, log=log, figure=False)
        pt.plot(xData=Ns, yData=theoryK1s, plotType=plotType2, xLab=xLab, yLab=yLab, title=title, legend=legend2, loc=1, log=log, figure=False)
        plt.errorbar(self.graphNs, rawK1s ,yerr=rawK1Errors, linestyle="None")
        plt.grid()
        if plotRatio: # Also plotting the ratio if specified
            yLab = r"$k_{1}^t / k_{1}^d$"
            title = "Ratio of Theoretical to Numerical k1 vs Network Size"
            legend = "Ratios"
            plt.figure(figsize=(12, 10))
            plt.axhline(y=1, linewidth=2, color = 'k')
            pt.plot(xData=self.graphNs, yData=ratios, plotType=plotType3, xLab=xLab, yLab=yLab, title=title, legend=legend, loc=1, log=logRatio, figure=False)
