import xml.etree.ElementTree as ET
from util import util
from valuations import read_xml as xml
from mediators.optimal_mediator.optimal_mediator import OptimalMediator
from valuations.scenario_factory import generate_uniform_random_scenario

random_scenario = False

if random_scenario:
    # Generate random scenario
    num_issues = 1
    domain_size = 5
    num_constraints = 5
    scenario_id = generate_uniform_random_scenario(num_issues, domain_size, num_constraints)
else:
    # Read scenario
    scenario_id = '4F45EC92D3'
    num_issues = 3
    domain_size = 4
    num_constraints = 9

print('Optimal mediator test for scenario id = ', scenario_id)
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')
u_funcs = xml.get_ufuns(scenario)

# TODO: data structure for bounds are inconsistent among multiple mediators. Should have the same data structure everywhere.
lower_bounds = [float(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
upper_bounds = [float(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]

# Run the mediator
optimal_mediator = OptimalMediator(num_issues=num_issues,
                                   num_agents=2,
                                   u_funcs=u_funcs,
                                   lower_bounds=lower_bounds,
                                   upper_bounds=upper_bounds,
                                   num_init_random_points=-1,
                                   num_random_restarts=-1,
                                   plot_mediator=False,
                                   verbose=False)
maximizer, max_value = optimal_mediator.mediate(-1)
print("Maximizer ", maximizer, ", max_value ", max_value)
