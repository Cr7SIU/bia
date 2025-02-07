create schema oltp;


create table oltp.user_transactions (
    user_id integer not null,
    amount integer not null,
    created_at timestamp without time zone not null default (current_timestamp at time zone 'utc')
);

CREATE SCHEMA Bronze;

CREATE TABLE bronze.post_codes_raw (
    postcode VARCHAR(255) NOT NULL,
    quality INTEGER NOT NULL,
    eastings INTEGER NOT NULL,
    northings INTEGER NOT NULL,
    country VARCHAR(255) NOT NULL,
    nhs_ha VARCHAR(255) NOT NULL,
    longitude FLOAT NOT NULL,
    latitude FLOAT NOT NULL,
    european_electoral_region VARCHAR(255) NOT NULL,
    primary_care_trust VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    lsoa VARCHAR(255) NOT NULL,
    msoa VARCHAR(255) NOT NULL,
    incode VARCHAR(255) NOT NULL,
    outcode VARCHAR(255) NOT NULL,
    parliamentary_constituency VARCHAR(255) NOT NULL,
    parliamentary_constituency_2024 VARCHAR(255) NOT NULL,
    admin_district VARCHAR(255) NOT NULL,
    parish VARCHAR(255) NOT NULL,
    admin_county VARCHAR(255) NOT NULL,
    date_of_introduction DATE NOT NULL,
    admin_ward VARCHAR(255) NOT NULL,
    ced VARCHAR(255) NOT NULL,
    ccg VARCHAR(255) NOT NULL,
    nuts VARCHAR(255) NOT NULL,
    pfa VARCHAR(255) NOT NULL,
    distance FLOAT NOT NULL,
    codes_admin_district VARCHAR(255) NOT NULL,
    codes_admin_county VARCHAR(255) NOT NULL,
    codes_admin_ward VARCHAR(255) NOT NULL,
    codes_parish VARCHAR(255) NOT NULL,
    codes_parliamentary_constituency VARCHAR(255) NOT NULL,
    codes_parliamentary_constituency_2024 VARCHAR(255) NOT NULL,
    codes_ccg VARCHAR(255) NOT NULL,
    codes_ccg_id VARCHAR(255) NOT NULL,
    codes_ced VARCHAR(255) NOT NULL,
    codes_nuts VARCHAR(255) NOT NULL,
    codes_lsoa VARCHAR(255) NOT NULL,
    codes_msoa VARCHAR(255) NOT NULL,
    codes_lau2 VARCHAR(255) NOT NULL,
    codes_pfa VARCHAR(255) NOT NULL,
    query_latitude FLOAT NOT NULL,
    query_longitude FLOAT NOT NULL
);