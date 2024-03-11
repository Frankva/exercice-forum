INSERT people (firstname, lastname)
VALUES
(?, ?);

INSERT emails (text, person_id)
VALUES
(?, (
        SELECT MAX(person_id)
        FROM people
));

INSERT passwords (hash, person_id)
VALUES
(?, (
        SELECT MAX(person_id)
        FROM people
));

