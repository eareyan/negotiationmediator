from valuations import read_xml
import xml.etree.ElementTree as ET
from util import util

scenario_id = '9611BA3D36'
num_issues = 2
domain_size = 9
num_constraints = 8
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')

u_funcs = read_xml.read_ufuns(scenario)

print("s=", read_xml.get_value_sum_hyperrect(u_funcs))

contract = (4, 4, 2)
print(read_xml.query_ufun(contract, 0, u_funcs) + read_xml.query_ufun(contract, 1, u_funcs))
contract = (4, 0, 2)
print(read_xml.query_ufun(contract, 0, u_funcs) + read_xml.query_ufun(contract, 1, u_funcs))

"""
# parse an xml file by name
scenarios = [ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-6.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-5.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-4.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-3.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-2.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1R4KW-6.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RC0I-1.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RC39-2.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RC39-4.xml'),
             ET.parse('/Users/enriqueareyan/Documents/workspace/bayesianmediator/scenarios/S-1Q1RF7V-1.xml')]

for scenario in scenarios:
    print('The scenario ID = ', scenario.getroot().attrib['id'])
    test_agents_u_fun = get_ufuns(scenario)
    contract = (18.0, 3.0, 3.0, 4.0, 18.0)
    for a in [0, 1]:
        print('\ttotal_value_agent_' + str(a) + ' = ', query_ufun(contract, a, test_agents_u_fun))"""

"""def f(x, u_funcs):
    print("X = ", x)
    return query_ufun(x, 0, u_funcs) + query_ufun(x, 1, u_funcs)"""

# u_funcs = get_ufuns(scenarios[0])
# print(f((6,), u_funcs))

"""import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 9, 400).reshape(-1, 1)
fx = np.array([f(x_i, u_funcs) for x_i in x])
plt.plot(x, fx, "r--", label="True (unknown)")
plt.show()"""
