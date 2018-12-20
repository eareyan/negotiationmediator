import sqlite3
from util import util
from ILP.welfare_max_nd import solve_welfare_max, complete_search
import xml.etree.ElementTree as ET


def check_mediator_result(cursor, db_scenario_id, mediator_id):
    cursor.execute("SELECT COUNT(*) FROM results WHERE scenario_id = " + str(db_scenario_id) + " AND mediator_id = " + str(mediator_id))
    mediator_scenario_res = cursor.fetchall()
    return mediator_scenario_res[0][0] == 0


def save_welfare_max_result(conn, cursor, scenario_id, mediator_id, welfare_max_contract, value_welfare_max_contract):
    cursor.execute("INSERT INTO results (scenario_id, mediator_id, welfare_max_contract, value_welfare_max_contract) "
                   "VALUES (" + str(scenario_id) + ", " + str(mediator_id) + ", '" + str(welfare_max_contract) + "', " + str(value_welfare_max_contract) + ")")
    conn.commit()


conn = sqlite3.connect(util.get_db_path() + 'results.db')
c = conn.cursor()

c.execute("SELECT * FROM scenarios")
r = c.fetchall()

for s in r:
    if check_mediator_result(c, s[0], 1):
        print("Computing welfare max for scenario: ", s[0], end='', flush=True)
        db_scenario_id = s[0]
        xml_id = s[1]
        num_issues = s[2]
        domain_size = s[3]
        num_constraints = s[4]

        scenario = ET.parse(util.get_scenario_path(num_issues, domain_size, num_constraints) + xml_id + '.xml')
        # maximizer, max_value = solve_welfare_max(scenario)
        maximizer, max_value = complete_search(scenario)
        save_welfare_max_result(conn, c, db_scenario_id, 1, maximizer, max_value)
        print("\t done!", end='\r', flush=True)
