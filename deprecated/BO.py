from skopt import gp_minimize
import xml.etree.ElementTree as ET
from valuations import read_xml as xml, scenario_factory
import util

# Generate a random scenario
num_issues = 2
domain_size = 15
num_constraints = 99
scenario_id = scenario_factory.generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
print("Generated ", scenario_id)
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')

# Get the utility functions from the scenarios
u_funcs = xml.read_ufuns(scenario)


# Define the welfare of two agents as the objective function
def f(the_x):
    return -1.0 * sum(xml.query_ufun(the_x, a, u_funcs) for a in range(0, 2))


# Get the bounds
bounds = xml.get_bounds(scenario)
print(bounds)

# Perform Bayesian optimization
res = gp_minimize(f,  # the function to minimize
                  bounds,  # the bounds on each dimension of x
                  acq_func="EI",  # the acquisition function
                  n_calls=15,  # the number of evaluations of f
                  n_random_starts=5,  # the number of random initialization points
                  noise=0.000000001,  # A very small noise number is equivalent to no noise, according to the documentation.
                  random_state=123,
                  verbose=False)

print("Welfare Max contract: ", res['x'], ", value of welfare max contract: ", res['fun'])
print(res)

# Some tests
""" File: S-1Q1RF7V-7.xml
a_contract = (6.416597884709046, 3.8562383356814323) # value = -186.0
print(xml.query_ufun(a_contract, 0, u_funcs))
print(xml.query_ufun(a_contract, 1, u_funcs))"""

""" File: S-1Q1RF7V-8.xml
a_contract = (0.0, 1.188070368621518, 7.42134106067379) # value = -160.0
print(xml.query_ufun(a_contract, 0, u_funcs))
print(xml.query_ufun(a_contract, 1, u_funcs))"""
