BEGIN;
DROP TABLE IF EXISTS "stamp";
CREATE TABLE "stamp" (
    "key" varchar(255) NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
)
;
COMMIT;
