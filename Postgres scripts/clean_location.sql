BEGIN;

-- removing "On or near " from location column
UPDATE london_crime_consolidated
SET location = REPLACE(location, 'On or near ', '');

COMMIT;