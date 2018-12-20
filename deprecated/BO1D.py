import numpy as np
import matplotlib.pyplot as plt
from skopt import gp_minimize
from valuations import read_xml as xml, scenario_factory
from skopt.plots import plot_convergence
from skopt.acquisition import gaussian_ei
import xml.etree.ElementTree as ET
from util import util

# Fix randomness so we can recreate experimental results
np.random.seed(123)
# Generate a random scenario with only one issue so that we can plot
num_issues = 1
domain_size = 10
num_constraints = 20
scenario_id = scenario_factory.generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
print("Generated ", scenario_id)

""" A single test """
scenario_id = '0AEBF84676'
num_issues = 1
domain_size = 10
num_constraints = 5
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')
u_funcs = xml.read_ufuns(scenario)

# Compute bounds
lower_bound = float(scenario.getroot()[0][0].attrib['lowerbound'])
upper_bound = float(scenario.getroot()[0][0].attrib['upperbound'])


# Define the welfare of two agents as the objective function
def f(the_x):
    return -1.0 * sum(xml.query_ufun(the_x, a, u_funcs) for a in range(0, 2))


n_calls = 30
n_random_starts = 5

# Perform Bayesian optimization
res = gp_minimize(f,  # the function to minimize
                  [(lower_bound, upper_bound)],  # the bounds on each dimension of x
                  acq_func="EI",  # the acquisition function
                  n_calls=n_calls,  # the number of evaluations of f
                  n_random_starts=n_random_starts,  # the number of random initialization points
                  noise=0.000000001,
                  random_state=123)  # the random seed

print("Welfare Max contract: ", res['x'], ", value of welfare max contract: ", res['fun'])

print("res = ", res)

plot_convergence(res)

mins = [np.min(res.func_vals[:i]) for i in range(1, n_calls + 1)]

print("mins = ", mins)
plt.rcParams["figure.figsize"] = (8, 14)

initial_num_true_func_samples = 4000
x = np.linspace(lower_bound, upper_bound, initial_num_true_func_samples).reshape(-1, 1)
x_gp = res.space.transform(x.tolist())
# fx = np.array([f(x_i) for x_i in x])

plt.show()
num_plots = 7

# Plot the num_plots iterations following the 5 random points
for n_iter in range(num_plots):
    gp = res.models[n_iter]
    curr_x_iters = res.x_iters[:num_plots + n_iter]
    curr_func_vals = res.func_vals[:num_plots + n_iter]

    print('Iteration', n_iter, ', curr_x_iters = ', curr_x_iters, ', curr_func_vals = ', curr_func_vals)

    # Plot true function.
    plt.subplot(num_plots, 2, 2 * n_iter + 1)
    # x = np.linspace(lowerbound, upperbound, initial_num_true_func_samples).reshape(-1, 1)
    fx = np.array([f(x_i) for x_i in x])
    plt.plot(x, fx, "r--", label="True (unknown)")
    # plt.plot([float(i) for i in range(0, int(upperbound))], [f((float(i),)) for i in range(0, int(upperbound))], "r--", label="True (unknown)")

    # Plot GP(x) + contours
    y_pred, sigma = gp.predict(x_gp, return_std=True)
    plt.plot(x, y_pred, "g--", label=r"$\mu_{GP}(x)$")
    plt.fill(np.concatenate([x, x[::-1]]),
             np.concatenate([y_pred - 1.9600 * sigma, (y_pred + 1.9600 * sigma)[::-1]]), alpha=.2, fc="g", ec="None")

    # Plot sampled points
    plt.plot(curr_x_iters, curr_func_vals, "r.", markersize=8, label="Observations")

    # Adjust plot layout
    plt.grid()

    if n_iter == 0:
        plt.legend(loc="best", prop={'size': 6}, numpoints=1)

    if n_iter != num_plots - 1:
        plt.tick_params(axis='x', which='both', bottom='off',
                        top='off', labelbottom='off')

    # Plot EI(x)
    plt.subplot(num_plots, 2, 2 * n_iter + 2)
    acq = gaussian_ei(x_gp, gp, y_opt=np.min(curr_func_vals))
    plt.plot(x, acq, "b", label="EI(x)")
    plt.fill_between(x.ravel(), -2.0, acq.ravel(), alpha=0.3, color='blue')

    next_x = res.x_iters[num_plots + n_iter]
    next_acq = gaussian_ei(res.space.transform([next_x]), gp, y_opt=np.min(curr_func_vals))
    plt.plot(next_x, next_acq, "bo", markersize=6, label="Next query point")

    # Adjust plot layout
    plt.ylim(0, 7)
    plt.grid()

    if n_iter == 0:
        plt.legend(loc="best", prop={'size': 6}, numpoints=1)

    if n_iter != num_plots - 1:
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

plt.show()
