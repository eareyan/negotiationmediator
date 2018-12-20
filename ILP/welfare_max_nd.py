import pulp
from valuations import read_xml as xml
import time
import math
import itertools


class InfeasibleILP(Exception):
    pass


def solve_welfare_max(scenario, verbose=False, bounds=None):
    u_funcs = xml.read_ufuns(scenario)
    num_issues = len(scenario.getroot()[0])

    L = [int(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
    U = [int(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]

    if verbose:
        print("Building model...")
        t0_building_model = time.time()

    v = {(a, i): h['height'] for a, H in u_funcs.items() for i, h in enumerate(H)}
    A = pulp.LpVariable.dicts('A', [(a, i, d) for d in range(0, num_issues) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
    B = pulp.LpVariable.dicts('B', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
    y = pulp.LpVariable.dicts('y', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
    l = pulp.LpVariable.dicts('l', [(a, i, d) for d in range(0, num_issues) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
    u = pulp.LpVariable.dicts('u', [(a, i, d) for d in range(0, num_issues) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)

    x = {d: pulp.LpVariable('x_' + str(d), lowBound=L[d], upBound=U[d], cat=pulp.LpInteger) for d in range(0, num_issues)}

    welfare_max_model = pulp.LpProblem("Welfare Max Model", pulp.LpMaximize)
    if bounds is not None:
        OBJ = pulp.LpVariable('OBJ', lowBound=0, cat=pulp.LpInteger)
        welfare_max_model += OBJ
        welfare_max_model += OBJ == sum([int(v[c]) * y[c] for c in v])
        # welfare_max_model += OBJ >= xml.get_value_max_hyperrect(u_funcs) # This constraint does not help.
        print("Bounds: (" + str(bounds[0]) + "," + str(bounds[1]) + ")")
        welfare_max_model += OBJ >= bounds[0]
        welfare_max_model += OBJ <= bounds[1]
    else:
        # print("No Bounds")
        welfare_max_model += sum([int(v[c]) * y[c] for c in v])

    for a, H in u_funcs.items():
        for i, h in enumerate(H):
            for d in range(0, num_issues):
                issue_index = 'issue_' + str(d + 1)
                h_dl = L[d] if issue_index not in h else h[issue_index]['min']
                h_du = U[d] if issue_index not in h else h[issue_index]['max']
                # if issue_index not in h:
                #    continue
                # if h_dl == L[d]:
                #    print("here", a, i, h, d,  issue_index)
                #    welfare_max_model += l[(a, i, d)] == 1
                # if h_du == U[d]:
                #    welfare_max_model += u[(a, i, d)] == 1
                # if h_dl == L[d] and h_du == U[d]:
                #    welfare_max_model += A[(a, i, d)] == 1
                welfare_max_model += x[d] >= h_dl - ((h_dl - L[d]) * (1 - y[(a, i)]))
                welfare_max_model += x[d] <= h_du + ((U[d] - h_du) * (1 - y[(a, i)]))
                welfare_max_model += A[(a, i, d)] >= l[(a, i, d)] + u[(a, i, d)] - 1
                welfare_max_model += A[(a, i, d)] <= l[(a, i, d)]
                welfare_max_model += A[(a, i, d)] <= u[(a, i, d)]
                welfare_max_model += x[d] >= h_dl - ((h_dl - L[d]) * (1 - l[(a, i, d)]))
                welfare_max_model += h_dl >= x[d] + 1 - ((U[d] + 1 - h_dl) * l[(a, i, d)])
                welfare_max_model += h_du >= x[d] - ((U[d] - h_du) * (1 - u[(a, i, d)]))
                welfare_max_model += x[d] >= h_du + 1 - ((h_du - L[d] + 1) * u[(a, i, d)])
                welfare_max_model += B[(a, i)] <= A[(a, i, d)]

            welfare_max_model += B[(a, i)] >= sum([A[(a, i, d)] for d in range(0, num_issues)]) - num_issues + 1
            welfare_max_model += B[(a, i)] <= y[(a, i)]

    # print(pulp.configSolvers())
    if verbose:
        print("Done building model, ", (time.time() - t0_building_model))
        print("Solving...")
        t0_solving_model = time.time()
    # Test available solvers
    # pulp.pulpTestAll()
    # I couldn't (yet) figure out how to connect with CPLEX...
    # welfare_max_model.solve(pulp.CPLEX_PY())
    welfare_max_model.solve()

    if verbose:
        print("Done solving model, ", (time.time() - t0_solving_model))
        print("Total time, ", (time.time() - t0_building_model))
        for a, H in u_funcs.items():
            for i, h in enumerate(H):
                print(a, i, y[(a, i)].value(), h['height'])
        print("Status:", pulp.LpStatus[welfare_max_model.status])
        for d in range(0, num_issues):
            print("x_" + str(d) + " value = ", x[d].value())
        print("Welfare: =", pulp.value(welfare_max_model.objective))

    # print(welfare_max_model)
    if pulp.LpStatus[welfare_max_model.status] != 'Optimal':
        if pulp.LpStatus[welfare_max_model.status] == 'Infeasible':
            raise InfeasibleILP("ILP was infeasible")
        else:
            raise Exception("ILP failed with status", pulp.LpStatus[welfare_max_model.status])
    return [x[d].value() for d in range(0, num_issues)], pulp.value(welfare_max_model.objective)


def halving_strategy(scenario, verbose=False):
    total = xml.get_value_sum_hyperrect(xml.read_ufuns(scenario))
    upper_bound = int(total)
    lower_bound = math.floor(upper_bound / 2.0)
    while lower_bound > 0:
        try:
            maximizer, max_value = solve_welfare_max(scenario, verbose, bounds=[lower_bound, upper_bound])
            return maximizer, max_value
        except Exception:
            upper_bound = lower_bound
            lower_bound = math.floor(lower_bound / 2.0)


def complete_search(scenario):
    u_funcs = xml.read_ufuns(scenario)
    num_issues = len(scenario.getroot()[0])
    L = [int(scenario.getroot()[0][i].attrib['lowerbound']) for i in range(0, num_issues)]
    U = [int(scenario.getroot()[0][i].attrib['upperbound']) for i in range(0, num_issues)]
    max_contract = None
    welfare_max = 0
    for x in itertools.product(*[[i for i in range(L[j], U[j] + 1)] for j in range(0, num_issues)]):
        welfare_at_x = sum([xml.query_ufun(x, a, u_funcs) for a in range(0, 2)])
        if welfare_at_x > welfare_max:
            max_contract = x
            welfare_max = welfare_at_x
    return [float(d) for d in max_contract], welfare_max
