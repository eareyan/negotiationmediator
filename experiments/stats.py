import sqlite3
# Student's t-test
from scipy.stats import ttest_ind
# Paired Student's t-test
from scipy.stats import ttest_rel
# Analysis of Variance test
from scipy.stats import f_oneway
from util import util
import pandas as pd

# Connect to the database
conn = sqlite3.connect(util.get_db_path() + 'results.db')
c = conn.cursor()
df = pd.read_sql_query(
    """
    SELECT  t.num_issues, t.domain_size, 
            AVG(poly2_to_opt), 
            AVG(poly3_to_opt), 
            AVG(poly4_to_opt), 
            AVG(bayes_to_opt), 
            AVG(bayes2_to_opt), 
            AVG(bayes3_to_opt),
            AVG(bayes4_to_opt) 
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
        r2.value_welfare_max_contract / r1.value_welfare_max_contract as poly2_to_opt,
        r3.value_welfare_max_contract / r1.value_welfare_max_contract as poly3_to_opt,
        r4.value_welfare_max_contract / r1.value_welfare_max_contract as poly4_to_opt,
        r5.value_welfare_max_contract / r1.value_welfare_max_contract as bayes_to_opt,
        r6.value_welfare_max_contract / r1.value_welfare_max_contract as bayes2_to_opt,
        r7.value_welfare_max_contract / r1.value_welfare_max_contract as bayes3_to_opt,
        r8.value_welfare_max_contract / r1.value_welfare_max_contract as bayes4_to_opt
    FROM results as r1 
        JOIN results as r2 
        JOIN results as r3
        JOIN results as r4
        JOIN results as r5
        JOIN results as r6
        JOIN results as r7
        JOIN results as r8
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
        AND r1.mediator_id = 1 
        AND r2.mediator_id = 2
        AND r3.mediator_id = 3
        AND r4.mediator_id = 4
        AND r5.mediator_id = 5
        AND r6.mediator_id = 6
        AND r7.mediator_id = 7
        AND r8.mediator_id = 8
        --AND r1.scenario_id = 377
        --AND s.num_issues = 5
        --AND s.domain_size = 9
        ) AS t
    --GROUP BY t.scenario_id, t.num_issues, t.domain_size, t.num_constraints
    --GROUP BY t.scenario_id, t.num_issues, t.domain_size
    --GROUP BY t.scenario_id, t.num_issues
    --GROUP BY t.scenario_id
    GROUP BY t.num_issues
    --GROUP BY t.domain_size
    --GROUP BY t.num_constraints
    """, conn)

print(df)

data1 = df['AVG(bayes_to_opt)']
data2 = df['AVG(poly2_to_opt)']

#data1 = df['AVG(bayes_to_opt)']
#data2 = df['AVG(poly3_to_opt)']

#data1 = df['AVG(bayes_to_opt)']
#data2 = df['AVG(poly4_to_opt)']

#data1 = df['AVG(bayes2_to_opt)']
#data2 = df['AVG(poly2_to_opt)']

data1 = df['AVG(bayes4_to_opt)']
data2 = df['AVG(poly2_to_opt)']

# No matter which test I use, the results are statistically significant. So far, poly (degree 2, 3, 4) > bayes except when domain size is 2.
# Also, different polys are indistinguishable, degree 2, 3, 4.

# compare samples
stat, p = ttest_rel(data1, data2)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distributions (fail to reject H0)')
else:
    print('Different distributions (reject H0)')

# compare samples
stat, p = ttest_ind(data1, data2)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distributions (fail to reject H0)')
else:
    print('Different distributions (reject H0)')

# compare samples
stat, p = f_oneway(data1, data2)
print('Statistics=%.3f, p=%.3f' % (stat, p))
# interpret
alpha = 0.05
if p > alpha:
    print('Same distributions (fail to reject H0)')
else:
    print('Different distributions (reject H0)')
