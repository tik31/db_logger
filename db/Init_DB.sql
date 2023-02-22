DROP DATABASE IF EXISTS Logger;
CREATE DATABASE Logger;
USE Logger;

#DROP TABLE IF EXISTS units;
#DROP TABLE IF EXISTS producers;
#DROP TABLE IF EXISTS parameters;
#DROP TABLE IF EXISTS levels;
#DROP TABLE IF EXISTS events;
#DROP TABLE IF EXISTS int_values;
#DROP TABLE IF EXISTS real_values;
#DROP TABLE IF EXISTS text_values;

CREATE TABLE units (
	id 				SERIAL PRIMARY KEY,
	name 			VARCHAR(255)
);

CREATE TABLE parameters (
	id 				SERIAL PRIMARY KEY,
	id_unit			BIGINT UNSIGNED NOT NULL,
	name 			VARCHAR(255),
	FOREIGN KEY (id_unit) REFERENCES units(id)
);

CREATE TABLE producers (
	id 				SERIAL PRIMARY KEY,
	name 			VARCHAR(255)
);

CREATE TABLE levels (
	id 				SERIAL PRIMARY KEY,
	name 			VARCHAR(255)
);

CREATE TABLE events (
	id 				SERIAL PRIMARY KEY,
	id_parameter	BIGINT UNSIGNED,
	id_level		BIGINT UNSIGNED,
	id_producer		BIGINT UNSIGNED,
	event_time 		DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (id_parameter) REFERENCES parameters(id),
	FOREIGN KEY (id_level) REFERENCES levels(id),
	FOREIGN KEY (id_producer) REFERENCES producers(id)
);

CREATE TABLE real_values (
	id				BIGINT UNSIGNED NOT NULL,
	value			REAL,
	FOREIGN KEY (id) REFERENCES events(id)
);

CREATE TABLE int_values (
	id				BIGINT UNSIGNED NOT NULL,
	value			INTEGER,
	FOREIGN KEY (id) REFERENCES events(id)
);

CREATE TABLE text_values (
	id				BIGINT UNSIGNED NOT NULL,
	value			VARCHAR(2047),
	FOREIGN KEY (id) REFERENCES events(id)
);

#INSERT INTO parameters (name) VALUES ('Channel 1 Voltage');
#INSERT INTO parameters (name) VALUES ('Channel 2 Voltage');
#INSERT INTO parameters (name) VALUES ('Channel 3 Voltage');
#INSERT INTO parameters (name) VALUES ('Channel 4 Voltage');

INSERT INTO units (name) VALUES ('unit');
INSERT INTO units (name) VALUES ('sec');
INSERT INTO units (name) VALUES ('V');
INSERT INTO units (name) VALUES ('A');
INSERT INTO units (name) VALUES ('LOGIC');

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
INSERT INTO producers (name) VALUES ('BO-M1');