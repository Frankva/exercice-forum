SELECT name
FROM authorization_groups
NATURAL JOIN person_belong_group
WHERE person_id=?;
