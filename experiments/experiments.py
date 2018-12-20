import sqlite3
import xml.etree.ElementTree as ET
from valuations import read_xml as xml, scenario_factory
from util import util
from mediators.optimal_mediator.optimal_mediator import OptimalMediator
from mediators.poly_mediator_individual.poly_mediator_individual import PolyMediatorIndividual
from mediators.bayes_mediator_social.bayes_mediator_social import BayesMediatorSocial
from mediators.gp_mediator_individual.gp_mediator_individual import GPMediatorIndividual
from mediators.gp_mediator_social.gp_mediator_social import GPMediatorSocial
from mediators.poly_mediator_social.poly_mediator_social import PolyMediatorSocial

# To create a polynomial kernel we need the following imports.
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import Exponentiation
from skopt.learning.gaussian_process.kernels import DotProduct
from skopt.learning.gaussian_process.kernels import Sum
from skopt.learning.gaussian_process.kernels import Product
from skopt.learning.gaussian_process.kernels import ConstantKernel

import sys
import warnings

warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")


def generate_bulk_scenarios(the_conn, cursor):
    # Test a number of issues...
    for the_num_issues in range(2, 6):
        # In some domain size...
        for the_domain_size in range(2, 10):
            # For some number of hyper-rectangles...
            for the_num_constraints in range(2, 10):
                cursor.execute("SELECT COUNT(*) FROM scenarios WHERE num_issues = " + str(the_num_issues) +
                               " AND domain_size = " + str(the_domain_size) + " AND num_constraints = " + str(the_num_constraints))
                data = cursor.fetchall()
                # Repeat the experiments a few times... (only as necessary)
                for t in range(0, max(0, 10 - data[0][0])):
                    # Generate a uniform random scenario
                    scenario_id = scenario_factory.generate_uniform_random_scenario(the_num_issues, the_domain_size, the_num_constraints)
                    # Print something so we know that there is progress
                    print("t = " + str(t) + ", num_issues = " + str(the_num_issues) + ", domain_size = " + str(the_domain_size) +
                          ", num_constraints = " + str(the_num_constraints) + ". Id = ", scenario_id)
                    cursor.execute("INSERT INTO scenarios (xml_file, num_issues, domain_size, num_constraints) "
                                   "VALUES (" + "'" + scenario_id + "'" + "," + str(the_num_issues) + "," + str(the_domain_size) + ", " + str(the_num_constraints) + ")")
                    the_conn.commit()


def save_mediator_result(the_conn, the_cursor, the_db_scenario_id, the_db_mediator_id, the_welfare_max_contract, the_value_welfare_max_contract):
    the_cursor.execute("INSERT INTO results (scenario_id, mediator_id, welfare_max_contract, value_welfare_max_contract) "
                       "VALUES (" + str(the_db_scenario_id) + ", " + str(the_db_mediator_id) + ", '" + str(the_welfare_max_contract) + "', " +
                       str(the_value_welfare_max_contract) + ")")
    the_conn.commit()


def check_mediator_result(cursor, the_db_scenario_id, the_db_mediator_id):
    cursor.execute("SELECT COUNT(*) FROM results WHERE scenario_id = " + str(the_db_scenario_id) + " AND mediator_id = " + str(the_db_mediator_id))
    mediator_scenario_res = cursor.fetchall()
    return mediator_scenario_res[0][0] == 0


# Connect to the database
conn = sqlite3.connect(util.get_db_path() + 'results.db')
c = conn.cursor()
# Generate the scenarios
# generate_bulk_scenarios(c)

# Select the scenarios from the database.
if len(sys.argv) > 1:
    c.execute("SELECT * FROM scenarios WHERE num_issues = 5 AND domain_size = " + str(sys.argv[1]))
else:
    c.execute("SELECT * FROM scenarios WHERE num_issues = 5")
r = c.fetchall()

"""
# For documentation purposes: here are the common parameters of the mediators I have used so far:
num_rounds = 10 
num_init_random_points = 10
num_random_restarts = 10
"""
num_rounds = 10
num_init_random_points = 10
num_random_restarts = 10


def mediator_triage(mediator_id, base_params_dict):
    # Mediator id 1 is the optimal
    if mediator_id == 1:
        return OptimalMediator(**base_params_dict)
    elif 2 <= mediator_id <= 4:
        # Poly Mediator Individual. Need to add an additional parameter for the degree of the polynomial.
        poly_mediator_params = base_params_dict.copy()
        poly_mediator_params['degree'] = mediator_id
        return PolyMediatorIndividual(**poly_mediator_params)
    elif mediator_id == 5:
        # Default Bayes Mediator. Does not take in any additional parameters.
        return BayesMediatorSocial(**base_params_dict)
    elif 6 <= mediator_id <= 8:
        # Polynomial Bayes Mediator, Social.
        base_mediator_params = base_params_dict.copy()
        base_mediator_params['base_estimator'] = \
            GaussianProcessRegressor(
                kernel=Exponentiation(Sum(Product(ConstantKernel(), DotProduct()), ConstantKernel(1.0, (0.01, 1000.0))), float(mediator_id) - 4.0),
                normalize_y=True,
                noise="gaussian",
                n_restarts_optimizer=2)
        return BayesMediatorSocial(**base_mediator_params)
    elif mediator_id == 9:
        # GP Mediator Individual with default kernel, which is the same as that used by BayesMediator (Mattern kernel).
        return GPMediatorIndividual(**base_params_dict)
    elif mediator_id == 10:
        # GP Mediator Social with default kernel, which is the same as that used by BayesMediator (Mattern kernel).
        return GPMediatorSocial(**base_params_dict)
    elif 11 <= mediator_id <= 13:
        poly_mediator_params = base_params_dict.copy()
        poly_mediator_params['degree'] = mediator_id - 9
        return PolyMediatorSocial(**poly_mediator_params)
    else:
        raise Exception('Unknown mediator with id = ', mediator_id)


mediators_id_to_name = {1: 'WelfareMax',
                        2: 'PolyMediatorIndividual2', 3: 'PolyMediatorIndividual3', 4: 'PolyMediatorIndividual4',
                        5: 'BayesMediatorSocial',
                        6: 'BayesMediatorSocial2', 7: 'BayesMediatorSocial3', 8: 'BayesMediatorSocial4',
                        9: 'GPMediatorIndividual',
                        10: 'GPMediatorSocial',
                        11: 'PolyMediatorSocial2', 12: 'PolyMediatorSocial3', 13: 'PolyMediatorSocial4'
                        }
for s in r:
    # Read parameters of the scenario.
    db_scenario_id, xml_id, num_issues, domain_size, num_constraints = s[0], s[1], s[2], s[3], s[4]
    lower_bounds = [0.0 for i in range(0, num_issues)]
    upper_bounds = [float(domain_size - 1) for i in range(0, num_issues)]
    scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + xml_id + '.xml')
    # Get the utility functions from the scenarios.
    u_funcs = xml.get_ufuns(scenario)
    # Construct the base parameters used by all mediators.
    mediator_base_params = dict([('num_issues', num_issues),
                                 ('num_agents', 2),
                                 ('u_funcs', u_funcs),
                                 ('lower_bounds', lower_bounds),
                                 ('upper_bounds', upper_bounds),
                                 ('num_init_random_points', num_init_random_points),
                                 ('num_random_restarts', num_random_restarts)])
    # Run each mediator.
    for mediator_db_id in range(1, 14):
        if check_mediator_result(c, db_scenario_id, mediator_db_id):
            print("Running ", mediators_id_to_name[mediator_db_id], " for \t", s, "...", end='', flush=True)
            the_mediator = mediator_triage(mediator_db_id, mediator_base_params)
            maximizer, max_value = the_mediator.mediate(num_rounds)
            save_mediator_result(conn, c, db_scenario_id, mediator_db_id, maximizer, max_value)
            print("\t done!", end='\r', flush=True)
        else:
            print("We have results for this pair: ", s, " for ", mediators_id_to_name[mediator_db_id])
# Close the database
conn.close()
