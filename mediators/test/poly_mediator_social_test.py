import xml.etree.ElementTree as ET
from util import util
from valuations import read_xml as xml
from mediators.poly_mediator_social.poly_mediator_social import PolyMediatorSocial
from valuations.scenario_factory import generate_uniform_random_scenario

random_scenario = True

if random_scenario:
    # Generate random scenario
    num_issues = 1
    domain_size = 5
    num_constraints = 5
    scenario_id = generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
else:
    # Read scenario
    scenario_id = '6D9AA1D636'
    num_issues = 1
    domain_size = 3
    num_constraints = 5

print('GP mediator social test for scenario id = ', scenario_id)
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')
u_funcs = xml.get_ufuns(scenario)

# TODO: data structure for bounds are inconsistent among multiple mediators. Should have the same data structure everywhere.
lower_bounds = [float(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
upper_bounds = [float(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]

# Run the mediator
degree = 3
num_init_random_points = 10
num_random_restarts = 10
poly_mediator_social = PolyMediatorSocial(num_issues=num_issues,
                                          num_agents=2,
                                          u_funcs=u_funcs,
                                          lower_bounds=lower_bounds,
                                          upper_bounds=upper_bounds,
                                          degree=degree,
                                          num_init_random_points=num_init_random_points,
                                          num_random_restarts=num_random_restarts,
                                          plot_mediator=num_issues == 1,
                                          verbose=True)
maximizer, max_value = poly_mediator_social.mediate(10)
print("Maximizer ", maximizer, ", max_value ", max_value)
