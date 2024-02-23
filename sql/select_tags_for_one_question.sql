SELECT name
FROM tags
NATURAL JOIN question_have_tag
WHERE question_id=?;
