DROP TABLE IF EXISTS units;
DROP TABLE IF EXISTS producers;
DROP TABLE IF EXISTS parameters;
DROP TABLE IF EXISTS levels;
DROP TABLE IF EXISTS events;
DROP TABLE IF EXISTS int_values;
DROP TABLE IF EXISTS real_values;
DROP TABLE IF EXISTS text_values;

CREATE TABLE units (
	id 				INTEGER PRIMARY KEY,
	name 			TEXT,
	table_name 		TEXT,
	comment			TEXT
);

CREATE TABLE parameters (
	id 				INTEGER PRIMARY KEY,
	id_unit			INTEGER,
	name 			TEXT,
	comment			TEXT,
	FOREIGN KEY (id_unit) REFERENCES units(id)
);

CREATE TABLE producers (
	id 				INTEGER PRIMARY KEY,
	name 			TEXT,
	comment			TEXT
);

CREATE TABLE levels (
	id 				INTEGER PRIMARY KEY,
	name 			TEXT,
	comment			TEXT
);

CREATE TABLE events (
	id 				INTEGER PRIMARY KEY AUTOINCREMENT,
	id_parameter	INTEGER,
	id_level		INTEGER,
	id_producer		INTEGER,
	event_time 		TEXT,
	int_values  	INTEGER,
	text_values 	TEXT,
	real_values 	REAL,
	FOREIGN KEY (id_parameter) REFERENCES parameters(id),
	FOREIGN KEY (id_level) REFERENCES levels(id),
	FOREIGN KEY (id_producer) REFERENCES producers(id)
);

CREATE TABLE real_values (
	id				INTEGER,
	value			REAL,
	FOREIGN KEY (id) REFERENCES events(id)
);

CREATE TABLE int_values (
	id				INTEGER,
	value			INTEGER,
	FOREIGN KEY (id) REFERENCES events(id)
);

CREATE TABLE text_values (
	id				INTEGER,
	value			TEXT,
	FOREIGN KEY (id) REFERENCES events(id)
);

INSERT INTO units (name, table_name) VALUES ('unit', 'int_values');
INSERT INTO units (name, table_name) VALUES ('sec', 'real_values');
INSERT INTO units (name, table_name) VALUES ('V', 'real_values');
INSERT INTO units (name, table_name) VALUES ('A', 'real_values');
INSERT INTO units (name, table_name) VALUES ('LOGIC', 'int_values');

INSERT INTO parameters (name, id_unit) VALUES ('PWR_U', 3);
INSERT INTO parameters (name, id_unit) VALUES ('PWR_I', 4);

INSERT INTO parameters (name, id_unit) VALUES ('MB1', 3);
INSERT INTO parameters (name, id_unit) VALUES ('MB2', 3);
INSERT INTO parameters (name, id_unit) VALUES ('MB3', 3);
INSERT INTO parameters (name, id_unit) VALUES ('MB4', 3);
INSERT INTO parameters (name, id_unit) VALUES ('MB5', 3);

INSERT INTO parameters (name, id_unit) VALUES ('ADC_BOARD_1_PWR', 5);
INSERT INTO parameters (name, id_unit) VALUES ('ADC_BOARD_2_PWR', 5);
INSERT INTO parameters (name, id_unit) VALUES ('ADC_BOARD_3_PWR', 5);
INSERT INTO parameters (name, id_unit) VALUES ('ADC_BOARD_4_PWR', 5);

INSERT INTO levels (name) VALUES ('DATA');
INSERT INTO levels (name) VALUES ('INFO');
INSERT INTO levels (name) VALUES ('WARNING');
INSERT INTO levels (name) VALUES ('ERROR');
INSERT INTO levels (name) VALUES ('CRITICAL');

INSERT INTO producers (name) VALUES ('GENERATOR');
INSERT INTO producers (name) VALUES ('MULTIMETR');