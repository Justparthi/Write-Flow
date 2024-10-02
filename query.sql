CREATE TABLE blog (
	id SERIAL PRIMARY KEY,
	title VARCHAR(699),
	subtitle VARCHAR(699),
	body VARCHAR(69999),
	author VARCHAR(69),
	img_url VARCHAR(699),
	date VARCHAR(69)
)


CREATE TABLE register (
	id SERIAL PRIMARY KEY,
	email VARCHAR(699),
	password VARCHAR(699),
	name VARCHAR(69999)
)