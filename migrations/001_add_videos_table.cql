CREATE TABLE videos (
    id text,
    source text,
    description text,
    feed_id text,
    thumbnail_url text,
    PRIMARY KEY ((id, source))
);

CREATE TABLE feeds (
    id text,
    source text,
    url text,
    PRIMARY KEY ((id, source))
);



--//@UNDO
DROP TABLE feeds;
DROP TABLE videos;
