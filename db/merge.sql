SELECT 
	--s.id,
	s.num_issues as i,
	s.domain_size as s,
	s.num_constraints as c,
	r1.scenario_id as id,
	--r1.mediator_id,
	r1.welfare_max_contract as opt,
	r1.value_welfare_max_contract as opt_val, 
	--r2.mediator_id, 
	r2.welfare_max_contract as poly_2,
	r2.value_welfare_max_contract as poly_2_val,
	--r3.mediator_id, 
	r3.welfare_max_contract as poly_3,
	r3.value_welfare_max_contract as poly_3_val,
	--r4.mediator_id, 
	r4.welfare_max_contract as poly_4,
	r4.value_welfare_max_contract as poly_4_val,
	--r5.mediator_id, 
	r5.welfare_max_contract as bayes,
	r5.value_welfare_max_contract as bayes_val,
	r2.value_welfare_max_contract / r1.value_welfare_max_contract as bayes_to_opt,
	r3.value_welfare_max_contract / r1.value_welfare_max_contract as poly_to_opt
FROM results as r1 
	JOIN results as r2 
	JOIN results as r3
	JOIN results as r4
	JOIN results as r5
	JOIN scenarios as s
WHERE 
	r1.scenario_id = r2.scenario_id 
	AND r1.scenario_id = r3.scenario_id 
	AND r1.scenario_id = r4.scenario_id
	AND r1.scenario_id = r5.scenario_id
	AND r1.scenario_id = s.id
	AND r1.mediator_id = 1 
	AND r2.mediator_id = 2
	AND r3.mediator_id = 3
	AND r4.mediator_id = 4
	AND r5.mediator_id = 5
	--AND r1.scenario_id = 377
	--AND s.num_issues = 2
	--AND bayes_to_opt < poly_to_opt
