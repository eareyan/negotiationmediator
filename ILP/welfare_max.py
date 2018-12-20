import pulp
from util import util
import xml.etree.ElementTree as ET
from valuations import read_xml as xml

scenario_id = '0AEBF84676'
scenario_id = '1F447132EE'
scenario_id = '3B4B0890A8'
#scenario_id = '5FADEA4442'
num_issues = 1
domain_size = 10
num_constraints = 5
scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + scenario_id + '.xml')
u_funcs = xml.read_ufuns(scenario)

L = int(scenario.getroot()[0][0].attrib['lowerbound'])
U = int(scenario.getroot()[0][0].attrib['upperbound'])

v = {(a, i): h['height'] for a, H in u_funcs.items() for i, h in enumerate(H)}
A = pulp.LpVariable.dicts('A', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
y = pulp.LpVariable.dicts('y', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
l = pulp.LpVariable.dicts('l', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)
u = pulp.LpVariable.dicts('u', [(a, i) for a, H in u_funcs.items() for i, h in enumerate(H)], lowBound=0, upBound=1, cat=pulp.LpInteger)

x = pulp.LpVariable("x", lowBound=L, upBound=U, cat=pulp.LpInteger)

welfare_max_model = pulp.LpProblem("Welfare Max Model", pulp.LpMaximize)
welfare_max_model += sum([v[c] * y[c] for c in v])

for a, H in u_funcs.items():
    for i, h in enumerate(H):
        welfare_max_model += x >= h['issue_1']['min'] - ((h['issue_1']['min'] - L) * (1 - y[(a, i)]))
        welfare_max_model += x <= h['issue_1']['max'] + ((U - h['issue_1']['max']) * (1 - y[(a, i)]))
        welfare_max_model += A[(a, i)] >= l[(a, i)] + u[(a, i)] - 1
        welfare_max_model += A[(a, i)] <= l[(a, i)]
        welfare_max_model += A[(a, i)] <= u[(a, i)]
        welfare_max_model += A[(a, i)] <= y[(a, i)]
        welfare_max_model += x >= h['issue_1']['min'] - ((h['issue_1']['min'] - L) * (1 - l[(a, i)]))
        welfare_max_model += h['issue_1']['min'] >= x + 1 - ((U + 1 - h['issue_1']['min']) * l[(a, i)])
        welfare_max_model += h['issue_1']['max'] >= x - ((U - h['issue_1']['max']) * (1 - u[(a, i)]))
        welfare_max_model += x >= h['issue_1']['max'] + 1 - ((h['issue_1']['max'] - L + 1) * u[(a, i)])

welfare_max_model.solve()
for a, H in u_funcs.items():
    for i, h in enumerate(H):
        print(a, i, y[(a, i)].value(), h['height'])
print("Status:", pulp.LpStatus[welfare_max_model.status])
print("x value = ", x.value())
print("Welfare: =", pulp.value(welfare_max_model.objective))
