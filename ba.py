import numpy as np
import scipy as sp
import random
import copy
import itertools
from matplotlib import pyplot as plt
import networkx as nx

class BA:

    def __init__(self, m, N, L):

        self.m = m
        self.N = N
        self.L = L
        self.n0 = self.m + 1
        self.G = nx.complete_graph(self.n0)
        self.edges = self.G.edges()
        self.nodes = self.G.nodes()
        self.newEdges = []
        self.newNodes = []
        self.neighbours = [self.G.neighbors(n) for n in self.nodes]
        self.newNeighbours = []

    def getM(self):
        """ Returns the m value """

        return self.m

    def getN(self):
        """ Returns the N value """

        return self.N

    def getL(self):
        """ Returns the L value """

        return self.L

    def getn0(self):
        """ Returns the n0 value """

        return self.n0

    def getNodes(self):
        """ Returns all the nodes currently in the graph """

        return self.G.nodes()

    def getEdges(self):
        """ Returns all the edges currently in the graph """

        return self.G.edges()

    def getDegrees(self, values=False, sort=False):
        """ Returns the degrees values of all nodes currently in the graph """

        if values:
            if sort:
                return sorted(nx.degree(self.G).values())
            else:
                return nx.degree(self.G).values()
        else:
            return nx.degree(self.G)

    def addNewEdges(self):
        """ Appending the new edges via networkx """

        self.G.add_edges_from(self.newEdges)

    def newNode(self, value):
        """ Adding a new node to the graph. Also adds a new neighbours adjacency list """

        self.nodes.append(value)
        self.newNodes.append(value)
        self.neighbours.append([])

    def addNewNodes(self):
        """ Appending the new nodes via networkx """

        self.G.add_nodes_from(self.newNodes)

    def getNeighbours(self):
        """ Returns the adjacency list of neighbours for all nodes """

        return self.neighbours

    def attachNewNeighbours(self):
        """ Appends the new neighbours to their corresponding adjacency lists """

        for edge in self.newNeighbours:
            firstNode = edge[0]
            secondNode = edge[1]
            self.neighbours[firstNode].append(secondNode)
            self.neighbours[secondNode].append(firstNode)

        del self.newNeighbours[:]

    def addConnections(self):
        """ Adds new edges via Phase 1 """

        edges = self.edges
        newNode = self.nodes[-1]

        randomNodes = []
        count = 0

        while count < self.m: # Randomly picking nodes until m different nodes are selected
            randomEdge = random.choice(edges) # Choosing a random edge from the edge list
            randomNode = random.choice(randomEdge) # Choosing a random node in the selected edge
            if randomNode not in randomNodes: # Avoiding duplicate edges
                count += 1
                randomNodes.append(randomNode)
            else:
                pass

        for randomNode in randomNodes: # Appending the new edges
            self.edges.append((newNode, randomNode))
            self.newEdges.append((newNode, randomNode))

    def addRandomConnections(self):
        """ Adds new edges via Phase 2 """

        edges = self.edges
        newNode = self.nodes[-1]

        randomNodes = []
        count = 0

        while count < self.m: # Randomly picking nodes until m different nodes are selected
            oldNodes = self.nodes[:-1]
            randomNode = random.choice(oldNodes) # Uniformly choosing a random node
            if randomNode not in randomNodes: # Avoiding duplicate edges
                count += 1
                randomNodes.append(randomNode)
            else:
                pass

        for randomNode in randomNodes: # Appending the new edges
            self.edges.append((newNode, randomNode))
            self.newEdges.append((newNode, randomNode))

    def addWalkConnections(self):
        """ Adds new edges via Phase 3 """

        edges = self.edges
        newNode = self.nodes[-1]

        randomNodes = []
        count = 0

        while count < self.m: # Randomly picking nodes until m different nodes are selected
            oldNodes = self.nodes[:-1]
            randomNode = random.choice(oldNodes) # Uniformly choosing a random node
            if self.L != 0: # Checking if the random walk length is not zero
                for i in range(self.L): # Iterating over the random walk length
                    randomNodeNeighbours = self.neighbours[randomNode] # Getting the neighbours of the current node location
                    randomNode = random.choice(randomNodeNeighbours) # Randomly choosing one of the neighbours
            elif self.L == 0:
                pass

            if randomNode not in randomNodes: # Avoiding duplicate edges
                count += 1
                randomNodes.append(randomNode)
            else:
                pass

        for randomNode in randomNodes: # Appending the new edges
            self.edges.append((newNode, randomNode))
            self.newEdges.append((newNode, randomNode))
            self.newNeighbours.append([newNode, randomNode])

        self.attachNewNeighbours() # Storing the new neighbours in their corresponding adjacency lists

    def showGraph(self):
        """ Draws the network visually if required """

        nx.draw_networkx(self.G)
        plt.show()

    def clearGraph(self):
        """ Removes all edges and nodes from the graph """

        self.G.clear()
