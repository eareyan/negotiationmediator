import xml.etree.ElementTree as ET
from util import util
from valuations import read_xml as xml


def f(p1, p2):
    print("p1 = ", p1)
    print("p2 = ", p2)


print(f(1, 2))

print({1:2}.items())
exit()

scenario = ET.parse(util.get_scenario_path(5, 5, 5) + 'C25F2639FE' + '.xml')
u_funcs = xml.read_ufuns(scenario)

contract = (2.0, 3.0, 1.0, 3.0, 3.0)
contract = (1.9, 4.0, 4.0, 4.0, 4.0)
contract = (2.2, 1.2, 1.9, 2.7, 3.6)
agent_1_value = xml.query_ufun(contract, 0, u_funcs)
agent_2_value = xml.query_ufun(contract, 1, u_funcs)

print(agent_1_value + agent_2_value)
exit()

from typing import List

print("test")


class Test:
    L: List[int] = []

    def __init__(self, n: int):
        self.L.append(n)
        print(id(self.L))


t = Test(1.7)
print(t)
print(t.L)

t = Test(2)
print(t)
print(t.L)

exit()

import numpy as np
from matplotlib import pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

np.random.seed(1)


def f(x):
    """The function to predict."""
    return x * np.cos(x)


def fit_GP(X):
    # Observations
    y = f(X).ravel()

    # Mesh the input space for evaluations of the real function, the prediction and
    # its MSE
    x = np.atleast_2d(np.linspace(0, 10, 1000)).T

    # Instantiate a Gaussian Process model
    kernel = C(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)

    # Fit to data using Maximum Likelihood Estimation of the parameters
    gp.fit(X, y)

    # Make the prediction on the meshed x-axis (ask for MSE as well)
    y_pred, sigma = gp.predict(x, return_std=True)
    return x, y, y_pred, sigma


def my_plot(x, y, y_pred, sigma):
    # Plot the function, the prediction and the 95% confidence interval based on
    # the MSE
    plt.figure()
    plt.plot(x, f(x), 'r:', label=u'$f(x) = x\,\sin(x)$')
    plt.plot(X, y, 'r.', markersize=10, label=u'Observations')
    plt.plot(x, y_pred, 'b-', label=u'Prediction')
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma,
                             (y_pred + 1.9600 * sigma)[::-1]]),
             alpha=.5, fc='b', ec='None', label='95% confidence interval')
    plt.xlabel('$x$')
    plt.ylabel('$f(x)$')
    plt.ylim(-10, 20)
    plt.legend(loc='upper left')

    plt.show()


"""for i in range(2, 12):
    X = np.atleast_2d([j for j in range(1, i)]).T
    x, y, y_pred, sigma = fit_GP(X)
    my_plot(x, y, y_pred, sigma)"""
