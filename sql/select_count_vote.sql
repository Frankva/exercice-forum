SELECT (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    NATURAL JOIN question_have_message
    WHERE (is_upvote=true) AND (question_id=?)
) - (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    NATURAL JOIN question_have_message
    WHERE (is_upvote=false) AND (question_id=?)
) AS vote;
