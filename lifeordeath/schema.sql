BEGIN;
DROP TABLE IF EXISTS "stamp";
CREATE TABLE "stamp" (
    "key" varchar(255) NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
)
;
CREATE INDEX "stamp_key_idx" ON stamp(key);
COMMIT;
