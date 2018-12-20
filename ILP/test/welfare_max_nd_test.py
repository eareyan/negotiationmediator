from util import util
import xml.etree.ElementTree as ET
from valuations.scenario_factory import generate_uniform_random_scenario
from ILP.welfare_max_nd import solve_welfare_max, halving_strategy, complete_search

scenario_id = '2C35721AC5'
num_issues = 2
domain_size = 9
num_constraints = 2

scenario_id = '8ED7DECFFE'
num_issues = 2
domain_size = 9
num_constraints = 3

# scenario_id = 'A93F91A6B1'
# num_issues = 2
# domain_size = 9
# num_constraints = 3

# scenario_id = '0A035DAC11'
# num_issues = 5
# domain_size = 9
# num_constraints = 9

# scenario_id = '21A89C78E3'
# num_issues = 2
# domain_size = 2
# num_constraints = 3


# scenario_id = '9EE0527DCA'
# num_issues = 2
# domain_size = 2
# num_constraints = 100

num_issues = 1
domain_size = 3
num_constraints = 5
scenario_id = '6D9AA1D636'
# scenario_id = generate_uniform_random_scenario(num_issues, domain_size, num_constraints)

scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')

import time

halving = True
print("Ready to start solving scenario ", scenario_id)
print("num_issues = ", num_issues)
print("domain_size = ", domain_size)
print("num_constraints = ", num_constraints)
t0 = time.time()
# if halving:
# maximizer, max_value = halving_strategy(scenario)
# else:
#maximizer, max_value = solve_welfare_max(scenario, bounds=(100, 1000))
maximizer, max_value = solve_welfare_max(scenario, verbose=True)
t1 = time.time()
print("Done!")
print(maximizer, max_value)
print(t1 - t0)

# complete_search(scenario)

exit()


import sqlite3
import pandas as pd

conn = sqlite3.connect(util.get_db_path() + 'results.db')
c = conn.cursor()

df = pd.read_sql_query(
    """
    SELECT * FROM scenarios JOIN results WHERE results.scenario_id = scenarios.id AND mediator_id = 1
    """, conn)
df[['value_welfare_max_contract']] = df[['value_welfare_max_contract']].astype('float')
for i, r in df.iterrows():
    print(r['xml_file'], r['num_issues'], r['domain_size'], r['num_constraints'], r['welfare_max_contract'], r['value_welfare_max_contract'])
    num_issues = r['num_issues']
    domain_size = r['domain_size']
    num_constraints = r['num_constraints']
    scenario_id = r['xml_file']

    scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')

    complete_search_max_contract, complete_search_max_value = complete_search(scenario)
    ILP_maximizer, ILP_max_value = solve_welfare_max(scenario)
    print("CS: ", complete_search_max_value, complete_search_max_contract, ", ILP: ", ILP_maximizer, ILP_max_value)
    # if complete_search_max_value != r['value_welfare_max_contract']:
    #    raise Exception("!")
    if complete_search_max_value != ILP_max_value:
        raise Exception("!")
