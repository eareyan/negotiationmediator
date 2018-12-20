import xml.etree.ElementTree as ET
from util import util
from valuations import read_xml as xml
from mediators.bayes_mediator_social.bayes_mediator_social import BayesMediatorSocial
from valuations.scenario_factory import generate_uniform_random_scenario
# To create a polynomial kernel we need the following imports.
from skopt.learning import GaussianProcessRegressor
from skopt.learning.gaussian_process.kernels import Exponentiation
from skopt.learning.gaussian_process.kernels import DotProduct
from skopt.learning.gaussian_process.kernels import Sum
from skopt.learning.gaussian_process.kernels import Product
from skopt.learning.gaussian_process.kernels import ConstantKernel

random_scenario = False

if random_scenario:
    # Generate random scenario
    num_issues = 2
    domain_size = 5
    num_constraints = 8
    scenario_id = generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
else:
    # Read scenario
    scenario_id = '17D8316EE9'
    num_issues = 1
    domain_size = 10
    num_constraints = 5

print('Bayesian mediator social for scenario id = ', scenario_id)
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')
u_funcs = xml.get_ufuns(scenario)

# TODO: data structure for bounds are inconsistent among multiple mediators. Should have the same data structure everywhere.
lower_bounds = [float(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
upper_bounds = [float(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]

# Run the mediator
num_init_random_points = 1
num_random_restarts = 5
base_estimator = GaussianProcessRegressor(kernel=Exponentiation(Sum(Product(ConstantKernel(), DotProduct()), ConstantKernel(1.0, (0.01, 1000.0))), 2.0),
                                          normalize_y=True,
                                          noise="gaussian",
                                          n_restarts_optimizer=2)
base_estimator = None
bayes_mediator_social = BayesMediatorSocial(num_issues=num_issues,
                                            num_agents=2,
                                            u_funcs=u_funcs,
                                            lower_bounds=lower_bounds,
                                            upper_bounds=upper_bounds,
                                            num_init_random_points=num_init_random_points,
                                            num_random_restarts=num_random_restarts,
                                            base_estimator=base_estimator,
                                            plot_mediator=num_issues == 1,
                                            verbose=True)
maximizer, max_value = bayes_mediator_social.mediate(10)
print("Maximizer ", maximizer, ", max_value ", max_value)
