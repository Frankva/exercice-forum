SELECT (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    WHERE (is_upvote=true) AND (message_id=3)
) - (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    WHERE (is_upvote=false) AND (message_id=3)
) AS vote;
