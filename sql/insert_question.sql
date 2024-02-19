START TRANSACTION;

INSERT INTO questions (title)
VALUES
('titre de la question');

INSERT INTO messages (text)
VALUES
('corps de la question');

INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));

INSERT INTO tags (name)
VALUES
('nom-du-tag');

INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions),
        (SELECT MAX(tag_id) FROM tags));

COMMIT;

-- if fail
ROLLBACK;
START TRANSACTION;
INSERT INTO questions (title)
VALUES
('titre de la question');

INSERT INTO messages (text)
VALUES
('corps de la question');

INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));


INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions),
        (SELECT tag_id FROM tags WHERE name='nom-du-tag'));

COMMIT;

-- string

START TRANSACTION;
INSERT INTO questions (title)
VALUES
(?);
INSERT INTO messages (text)
VALUES
(?);
INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));
INSERT INTO TAGS (name)
VALUES
(?);
INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions),
        (SELECT MAX(tag_id) FROM tags));
COMMIT;

-- if fail

ROLLBACK;
START TRANSACTION;
INSERT INTO questions (title)
VALUES
(?);
INSERT INTO messages (text)
VALUES
(?);
INSERT INTO question_have_message (question_id, message_id)
VALUES
((SELECT MAX(question_id) FROM questions),
    (SELECT MAX(message_id) FROM messages));
INSERT INTO question_have_tag (question_id, tag_id)
VALUES
((SELECT MAX(question_id) FROM questions),
        (SELECT tag_id FROM tags WHERE name=?));
COMMIT;
