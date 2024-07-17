BEGIN;

-- Add new column for date with type DATE
ALTER TABLE london_crime_consolidated
ADD COLUMN date_temp DATE;

-- Update new column date with converted values from the existing date column with text
UPDATE london_crime_consolidated
SET date_temp = to_date(date, 'YYYY-MM');

-- Delete old column
ALTER TABLE london_crime_consolidated
DROP COLUMN date;

-- Rename new column to name date
ALTER TABLE london_crime_consolidated
RENAME COLUMN date_temp TO date;

COMMIT;