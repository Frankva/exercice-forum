SELECT is_upvote
FROM person_vote_message
NATURAL JOIN question_have_message
WHERE  (question_id=?) AND (person_id=?);
