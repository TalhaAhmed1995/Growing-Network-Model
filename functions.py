import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import random

"""This module is strictly used for the functions required to produce optimised fits and calculating parameters."""

def func1(k, m):
    """ Equation (13) in the report """

    return (2. * m*(m + 1.)) / (k * (k + 1.) * (k + 2.))

def func2(k, m):
    """ Equation (19) in the report """

    return (1. / (m + 1.)) * ((m / (m + 1.))**(k - m))

def func3(N, m):
    """ Equation (15) in the report """

    return -0.5 + np.sqrt(0.25 + (m*(m+1.)*N))
    # return m * np.sqrt(N)

def func4(N, m):
    """ Equation (20) in the report """

    return m + ((np.log(N))/(np.log(1. + 1./m)))
