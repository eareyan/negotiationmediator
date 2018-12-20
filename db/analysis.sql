SELECT *, r.mediator_id FROM results AS r INNER JOIN scenarios AS s ON r.scenario_id = s.id
WHERE s.num_issues = 2 AND s.domain_size = 2