import subprocess
import uuid
from util import util


def generate_random_scenario(num_issues, domain_size, num_constraints, dim_probs, width_probs):
    lisp_output = subprocess.check_output([util.get_lisp_compiler_path(),
                                           '-l',
                                           util.get_lisp_scenariogen_path(),
                                           '-e',
                                           "(enrique :numissues " + str(num_issues) +
                                           " :domainsize " + str(domain_size) +
                                           " :numconstraints " + str(num_constraints) +
                                           " :dimprobs '" + dim_probs +
                                           " :widthprobs '" + width_probs + ")"])
    lisp_id = lisp_output.decode("utf-8").strip()[1:-1]
    hex_id = uuid.uuid4().hex[:10].upper()
    subprocess.check_output(['mv',
                             util.get_scenario_path(num_issues, domain_size, num_constraints) + str(lisp_id) + '.xml',
                             util.get_scenario_path(num_issues, domain_size, num_constraints) + str(hex_id) + '.xml'])

    return hex_id


def generate_uniform_random_scenario(num_issues, domain_size, num_constraints):
    # A hypervolume cares about any number of possible issues uniformly at random
    # The width of hyervolumes is uniform at random among all possible widths
    return generate_random_scenario(num_issues, domain_size, num_constraints,
                                    '(' + ''.join('(' + str(i) + ' 1) ' for i in range(1, num_issues + 1)).strip() + ')',
                                    '(' + ''.join('(' + str(i) + ' 1) ' for i in range(1, domain_size + 1)).strip() + ')')
