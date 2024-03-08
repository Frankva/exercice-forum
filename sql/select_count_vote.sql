SELECT (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    WHERE (is_upvote=true) AND (message_id=?)
) - (
    SELECT count(person_vote_message_id)
    FROM person_vote_message
    WHERE (is_upvote=false) AND (message_id=?)
) AS vote;
