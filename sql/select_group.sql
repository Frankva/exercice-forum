SELECT name
FROM authorization_groups
NATURAL JOIN people
WHERE person_id=?;
