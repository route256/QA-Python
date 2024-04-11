-- +goose Up
-- +goose StatementBegin
CREATE TABLE IF NOT EXISTS devices (
    id          serial      PRIMARY KEY,
    platform    varchar(32) NOT NULL,
    user_id     bigint      NOT NULL,
    entered_at  timestamp   NOT NULL,
    removed     bool        DEFAULT false NOT NULL,
    created_at  timestamp   DEFAULT now() NOT NULL,
    updated_at  timestamp   DEFAULT now() NOT NULL
);

CREATE TABLE IF NOT EXISTS devices_events (
    id          serial      PRIMARY KEY,
    device_id   bigint,
    type        int2        NOT NULL,
    status      int2        NOT NULL,
    payload     jsonb,
    created_at  timestamp   DEFAULT now() NOT NULL,
    updated_at  timestamp   DEFAULT now() NOT NULL,

    FOREIGN KEY (device_id) REFERENCES devices (id)
);

CREATE SCHEMA IF NOT EXISTS test;

CREATE OR REPLACE FUNCTION test.random_platform() RETURNS varchar(32)
AS
$func$
DECLARE
    platform varchar(32)[] := ARRAY['Linux','Windows', 'Android','Ios'];
BEGIN
    RETURN platform[floor((random()*(5-1)+1))::int];
END
$func$
    LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION test.random_interval() RETURNS interval AS
$func$
DECLARE
    ins interval;
BEGIN
    SELECT random() * INTERVAL '7 days' INTO ins;
    RETURN ins;
END
$func$
    LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION test.korean_random_bool() RETURNS bool AS
$func$
DECLARE
    platform bool[] := ARRAY[False, False, False, False, False, False, True];
BEGIN
    RETURN platform[floor((random()*(8-1)+1))::int];
END
$func$
    LANGUAGE PLPGSQL;

CREATE OR REPLACE FUNCTION event_device_created()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
    AS
$func$
BEGIN
    INSERT INTO devices_events (device_id, type, status, payload, created_at, updated_at)
    SELECT NEW.id, 1, 2,  to_jsonb((select d from (select NEW.user_id, NEW.platform, NEW.entered_at) d)), NEW.created_at, NEW.updated_at;
    RETURN NEW;
END;
$func$;

CREATE TRIGGER event_device_created
    AFTER INSERT
    ON devices
    FOR EACH ROW
EXECUTE PROCEDURE event_device_created();

CREATE OR REPLACE FUNCTION event_device_removed()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$func$
BEGIN
    IF NEW.removed THEN
        INSERT INTO devices_events (device_id, type, status, payload, created_at, updated_at)
        SELECT NEW.id, 1, 1, 'null', NEW.created_at, NEW.updated_at;
    END IF;
    RETURN NEW;
END;
$func$;

CREATE TRIGGER event_device_removed_update
    AFTER UPDATE
    ON devices
    FOR EACH ROW
EXECUTE PROCEDURE event_device_removed();

CREATE TRIGGER event_device_removed_insert
    AFTER INSERT
    ON devices
    FOR EACH ROW
EXECUTE PROCEDURE event_device_removed();

CREATE OR REPLACE FUNCTION event_device_updated()
    RETURNS TRIGGER
    LANGUAGE PLPGSQL
AS
$func$
BEGIN
    INSERT INTO devices_events (device_id, type, status, payload, created_at, updated_at)
    SELECT NEW.id, 2, 2, to_jsonb((SELECT d FROM (SELECT NEW.id, NEW.user_id, NEW.platform, NEW.created_at, NEW.updated_at) d)),
           NEW.created_at, NEW.updated_at;

    RETURN NEW;
END;
$func$;

CREATE TRIGGER event_device_updated
    AFTER UPDATE
    ON devices
    FOR EACH ROW
EXECUTE PROCEDURE event_device_updated();

BEGIN;
DO $insert$
    BEGIN
        INSERT INTO devices (platform, user_id, entered_at, removed, created_at, updated_at)
        SELECT test.random_platform(), random()*(1000-100)+100, entered_at, test.korean_random_bool(), entered_at - test.random_interval(), entered_at + test.random_interval()
        FROM generate_series(
                     now() - interval '1 month',
                     now() - interval '1 week',
                     INTERVAL '1 hour'
                 ) as entered_at ;
    END $insert$;
COMMIT;

BEGIN;
DO $update$
        DECLARE new_user_id bigint;
        DECLARE new_platform varchar(32);
    BEGIN
        new_user_id := 666;
        new_platform := 'Freebsd';

        UPDATE devices
        SET user_id = new_user_id, platform = new_platform
        WHERE EXTRACT(DAY FROM updated_at) = 13;
    END $update$;
COMMIT;


DROP TRIGGER IF EXISTS event_device_created ON devices;
DROP TRIGGER IF EXISTS event_device_removed_insert ON devices;
DROP TRIGGER IF EXISTS event_device_removed_update ON devices;
DROP TRIGGER IF EXISTS event_device_updated ON devices;
DROP FUNCTION IF EXISTS event_device_created();
DROP FUNCTION IF EXISTS event_device_updated();
DROP FUNCTION IF EXISTS event_device_removed();

-- +goose StatementEnd


-- +goose Down
TRUNCATE TABLE devices CASCADE;
DROP SCHEMA IF EXISTS test CASCADE ;