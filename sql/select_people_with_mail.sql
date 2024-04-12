SELECT person_id, firstname, lastname, text AS 'email'
FROM people
NATURAL JOIN emails;
