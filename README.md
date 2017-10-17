# Barabasi and Albert Growing Network Model

Networks usually possess two main attributes - vertices and edges. Vertices represent the objects/sites in the network, while the edges provide a means of linking vertices. Together, collections of these are referred to as graphs. For this investigation, a simple network was chosen, whereby the graph consists of edges that are undirected - no direction given to edges; unweighted - no relative strength of connections; and no self-loops - no edges starting and ending at the same site.

The system comprised of an initial network at time `t0`, which was constructed as a complete graph, such that all existing vertices were connected to every other vertex in the network via an edge. Thereafter, each time increment introduced a single new vertex, with `m` new edges; one end connected to the new entity, while the other was appended to an existing vertex, chosen with probability `Π`. The entire process was iterated multiple times until a total number of `N` vertices occupied the network space.

## How to use

Note that you will need to install the `networkx` python library in order to run this model.

In order to get the results simply run the `main.py` module. This module imports 3 of the other modules and runs a script to produce the results. Make sure that all the files are kept in one folder. Remember to change the directory to the folder containing all the files so that they can be identified and read.

All plots and calculated values as featured in the report cannot be replicated exactly, due to the random nature of the model, but similar results can be produced. It is recommended that you keep the number of loops `<= 3`. Also keep `N <= 10,000`, as larger values can take long to run.

`Lines 13` to `16` will allow you to change the type of model being investigating using simple Boolean arguments. Also look at `lines 18` to `26` to change specific parameters. `Line 29` allows you to change the number of loops, while `line 31` enables you to vary the length of the random walk if Phase 3 (see report) is being investigated.

NOTE: AFTER RUNNING, IT CAN TAKE UP TO 5 MINUTES FOR RESULTS TO APPEAR.

After running, the values of the `chi squared` test statistic for all graph sizes, along with the raw and theoretical `k1` values (if specified) will be output on the terminal. If `m` is being varied, 2 plots will be produced. On the other hand, if `N` is being varied, 5 plots will appear after the simulation.

Example output by only setting `multiN = True` on `line 14` and using `m = 3`, `NminPower = 2` and `NmaxPower = 5` on `lines 24` to `26`:

```
Fat Tail Removed?  False
Chi Values:  [ 42.152563  122.33496  632.85004  1844.8054]
p Values:  [ 0.00021291866  4.6381509e-11  5.445231e-86  1.287761e-273]
Fat Tail Removed?  True
Chi Values:  [ 16.66655  47.22752  75.384166  201.71999]
p Values:  [ 0.21499924  0.040453447  0.30857086  0.0050583538]
Theory K1s:  [   34.1446244    109.04565258   345.91052236  1094.94522912]
Numerical K1s:  [   26.    74.   344.  1254.]
Ratios:  [ 1.31325478  1.4735899   1.00555384  0.87316206]
33.8613858223
```

You can also play around with the `showGraph()` method in the `BA` class, which produces a visual representation of all the nodes and edges in the graph.

## Example Network Graphs

Below shows an initial graph with `m = 3`, and the same graph after there are `100` nodes on the graph.

![Initial graph with m=3.](/images/figure_1.png?raw=true)
![Graph after 100 nodes occupy the network.](/images/figure_2.png?raw=true)
