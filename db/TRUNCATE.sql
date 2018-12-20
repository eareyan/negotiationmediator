DELETE FROM results;    
DELETE FROM sqlite_sequence WHERE name = 'results';
--SELECT * FROM results WHERE bo_value_max_contract != '-Infinity'