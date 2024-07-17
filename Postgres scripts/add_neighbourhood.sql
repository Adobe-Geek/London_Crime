BEGIN;

ALTER TABLE london_crime_consolidated
ADD COLUMN neighbourhood TEXT;

COMMIT;