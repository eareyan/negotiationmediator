import xml.etree.ElementTree as ET
from util import util
from valuations import read_xml as xml
from mediators.poly_mediator_individual.poly_mediator_individual import PolyMediatorIndividual
from valuations.scenario_factory import generate_uniform_random_scenario
from valuations.paraboloid import get_paraboloid_lower_bounds, get_paraboloid_upper_bounds, get_paraboloid_ufuns

random_scenario = False

if random_scenario:
    # Generate random scenario
    num_issues = 2
    domain_size = 5
    num_constraints = 5
    scenario_id = generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
else:
    # Read scenario
    scenario_id = '6D9AA1D636'
    num_issues = 1
    domain_size = 3
    num_constraints = 5

print('Poly mediator test for scenario id = ', scenario_id)
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')

# TODO: data structure for bounds are inconsistent among multiple mediators. Should have the same data structure everywhere.
lower_bounds = [float(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
upper_bounds = [float(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]

# Run the mediator
degree = 5
num_init_random_points = 100
num_random_restarts = 10
poly_mediator_individual = PolyMediatorIndividual(num_issues=2,
                                                  # num_issues=num_issues,
                                                  num_agents=2,
                                                  # u_funcs=xml.get_ufuns(scenario),
                                                  u_funcs=get_paraboloid_ufuns(),
                                                  lower_bounds=get_paraboloid_lower_bounds(),
                                                  upper_bounds=get_paraboloid_upper_bounds(),
                                                  # lower_bounds=lower_bounds,
                                                  # upper_bounds=upper_bounds,
                                                  degree=degree,
                                                  num_init_random_points=num_init_random_points,
                                                  num_random_restarts=num_random_restarts,
                                                  # plot_mediator=num_issues == 1,
                                                  plot_mediator=False,
                                                  verbose=True)
maximizer, max_value = poly_mediator_individual.mediate(10)
print("Maximizer ", maximizer, ", max_value ", max_value)
