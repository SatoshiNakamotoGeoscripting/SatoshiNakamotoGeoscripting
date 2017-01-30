DROP TABLE trumptweets;
CREATE TABLE trumptweets (
    id  	bigint,
    time	varchar(500),
    latitude	decimal,
    longitude	decimal,
    selfrepcity varchar(500),    
    lang	varchar(500),
    source	varchar(500),
    countrycode	varchar(500),
    countryname	varchar(500),
    location	varchar(500),
    hyperling	varchar(500),
    text        varchar(500),
    outlat 	decimal,
    outlon	decimal
);
