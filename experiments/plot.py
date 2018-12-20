import sqlite3
from util import util
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
conn = sqlite3.connect(util.get_db_path() + 'results.db')
c = conn.cursor()


def get_grouped_data(group_by_cols):
    return pd.read_sql_query(
        """
        SELECT t.num_issues, t.domain_size, t.num_constraints, 
        AVG(poly2_to_opt), 
        AVG(poly3_to_opt), 
        AVG(poly4_to_opt), 
        AVG(bayes_to_opt),
        AVG(bayes2_to_opt),
        AVG(bayes3_to_opt),
        AVG(bayes4_to_opt),
        AVG(gp_to_opt)
        FROM(
        SELECT 
            r1.scenario_id,
            s.num_issues,
            s.domain_size,
            s.num_constraints,
            r1.value_welfare_max_contract as opt, 
            r2.value_welfare_max_contract as poly2,
            r3.value_welfare_max_contract as poly3,
            r4.value_welfare_max_contract as poly4,
            r5.value_welfare_max_contract as bayes,
            r6.value_welfare_max_contract as bayes2,
            r7.value_welfare_max_contract as bayes3,
            r8.value_welfare_max_contract as bayes4,
            r9.value_welfare_max_contract as gp,
            r2.value_welfare_max_contract / r1.value_welfare_max_contract as poly2_to_opt,
            r3.value_welfare_max_contract / r1.value_welfare_max_contract as poly3_to_opt,
            r4.value_welfare_max_contract / r1.value_welfare_max_contract as poly4_to_opt,
            r5.value_welfare_max_contract / r1.value_welfare_max_contract as bayes_to_opt,
            r6.value_welfare_max_contract / r1.value_welfare_max_contract as bayes2_to_opt,
            r7.value_welfare_max_contract / r1.value_welfare_max_contract as bayes3_to_opt,
            r8.value_welfare_max_contract / r1.value_welfare_max_contract as bayes4_to_opt,
            r9.value_welfare_max_contract / r1.value_welfare_max_contract as gp_to_opt
        FROM 
                 results as r1 
            JOIN results as r2 
            JOIN results as r3
            JOIN results as r4
            JOIN results as r5
            JOIN results as r6
            JOIN results as r7
            JOIN results as r8
            JOIN results as r9
            JOIN scenarios as s
        WHERE 
                r1.scenario_id = s.id
            AND s.id = r2.scenario_id 
            AND s.id = r3.scenario_id 
            AND s.id = r4.scenario_id 
            AND s.id = r5.scenario_id 
            AND s.id = r6.scenario_id 
            AND s.id = r7.scenario_id 
            AND s.id = r8.scenario_id
            AND s.id = r9.scenario_id
            AND r1.mediator_id = 1 
            AND r2.mediator_id = 2
            AND r3.mediator_id = 3
            AND r4.mediator_id = 4
            AND r5.mediator_id = 5
            AND r6.mediator_id = 6
            AND r7.mediator_id = 7
            AND r8.mediator_id = 8
            AND r9.mediator_id = 9
            --AND r1.scenario_id = 377
            --AND s.num_issues = 5
            --AND s.domain_size = 9
            ) AS t
        GROUP BY """ + ', '.join(group_by_cols), conn)


image_location_folder = '/Users/enriqueareyan/Documents/workspace/negotiationmediator/data/'

mediators_id_to_name = {2: 'PolyMediator2', 3: 'PolyMediator3', 4: 'PolyMediator4',
                        5: 'BayesMediator',
                        6: 'BayesMediator2', 7: 'BayesMediator3', 8: 'BayesMediator4',
                        9: 'GPMediator'
                        }


def plot_agg1(col):
    data = get_grouped_data(col)
    data = data.set_index(col)
    data.reset_index()
    plt.plot(data['AVG(bayes_to_opt)'])
    plt.plot(data['AVG(gp_to_opt)'])
    for d in [2, 3, 4]:
        plt.plot(data['AVG(poly' + str(d) + '_to_opt)'])
    # for d in [2, 3, 4]:
    for d in [2, 3, 4]:
        plt.plot(data['AVG(bayes' + str(d) + '_to_opt)'])
    plt.xlabel(col)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.savefig(image_location_folder + "1-" + col[0] + ".png", bbox_inches="tight")
    plt.clf()
    # plt.show()


print("Plotting first graphs")
for c in [['num_issues'], ['domain_size'], ['num_constraints']]:
    print(c)
    plot_agg1(c)


def plot_agg2(c, index1_domain_size, nrows, ncols):
    plt.figure(figsize=(15.5, 7.5))
    for i in range(1, index1_domain_size):
        axes = plt.subplot(nrows, ncols, i)
        df = get_grouped_data(c)
        data = df.loc[df[c[0]] == (i + 1)]
        data = data.set_index([c[1]])
        plt.plot(data['AVG(bayes_to_opt)'])
        plt.plot(data['AVG(gp_to_opt)'])
        for d in [2, 3, 4]:
            plt.plot(data['AVG(poly' + str(d) + '_to_opt)'])
        for d in [2, 3, 4]:
            plt.plot(data['AVG(bayes' + str(d) + '_to_opt)'])
            axes.set_ylim(0, 1)
        plt.xlabel(c[1])
        plt.title(c[0] + ' = ' + str(i + 1))
    plt.tight_layout()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig(image_location_folder + "2-" + c[0] + "-" + c[1] + ".png", bbox_inches="tight")
    plt.clf()
    # plt.show()


plot_agg2(['num_issues', 'domain_size'], 5, 1, 4)
plot_agg2(['num_issues', 'num_constraints'], 5, 1, 4)

plot_agg2(['domain_size', 'num_constraints'], 9, 2, 4)
plot_agg2(['domain_size', 'num_issues'], 9, 2, 4)

plot_agg2(['num_constraints', 'domain_size'], 9, 2, 4)
plot_agg2(['num_constraints', 'num_issues'], 9, 2, 4)
