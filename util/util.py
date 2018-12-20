def get_scenario_path(num_issues, domain_size, num_constraints):
    return '/Users/enriqueareyan/Documents/workspace/negotiationmediator/scenarios/num_issues_' \
           + str(num_issues) + '/domain_size_' \
           + str(domain_size) + '/num_constraints_' \
           + str(num_constraints) + '/'


def get_db_path():
    return "/Users/enriqueareyan/Documents/workspace/negotiationmediator/db/"


def get_lisp_compiler_path():
    return "/Library/ccl/dx86cl64"

def get_lisp_scenariogen_path():
    return "/Users/enriqueareyan/Documents/workspace/negotiationmediator/lisp/scenariogen.lisp"
