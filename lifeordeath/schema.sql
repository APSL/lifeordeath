BEGIN;
DROP TABLE "stamp";
DROP TABLE "event";
CREATE TABLE "event" (
    "id" serial NOT NULL PRIMARY KEY,
    "key" varchar(255) NOT NULL,
    "frequency" integer NOT NULL,
    "warning" integer NOT NULL
)
;
CREATE TABLE "stamp" (
    "id" serial NOT NULL PRIMARY KEY,
    "event_id" integer NOT NULL REFERENCES "event" ("id") DEFERRABLE INITIALLY DEFERRED,
    "timestamp" timestamp without time zone NOT NULL
)
;
CREATE INDEX "stamp_event_id" ON "stamp" ("event_id");
COMMIT;
