BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `scenarios` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`xml_file`	TEXT NOT NULL,
	`num_issues`	INTEGER NOT NULL,
	`domain_size`	INTEGER NOT NULL,
	`num_constraints`	INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS `results` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`scenario_id`	INTEGER NOT NULL,
	`mediator_id`	INTEGER NOT NULL,
	`welfare_max_contract`	TEXT NOT NULL,
	`value_welfare_max_contract`	TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `mediators` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL
);
COMMIT;
