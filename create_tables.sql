
CREATE TABLE user (
        id INTEGER NOT NULL,
        username VARCHAR,
        firstName VARCHAR,
        lastName VARCHAR,
        email VARCHAR,
        password VARCHAR,
        phone VARCHAR,
        PRIMARY KEY (id),
        UNIQUE (username)
);

CREATE TABLE event (
        creatorid INTEGER,
        usersid INTEGER,
        eventid INTEGER NOT NULL,
        name VARCHAR,
        content VARCHAR,
        tags VARCHAR,
        date VARCHAR,
        PRIMARY KEY (eventid)
);
