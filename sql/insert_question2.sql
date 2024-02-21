
INSERT INTO questions (title)
VALUES
(?);
INSERT INTO messages (text, person_id)
VALUES
(?, ?);
INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));

SELECT tag_id
FROM tags
WHERE name=?;

INSERT INTO tags (name)
VALUES
(?);

INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions), 
        (SELECT tag_id FROM tags WHERE name=?));
