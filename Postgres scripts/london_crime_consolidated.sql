CREATE TABLE public.london_crime_consolidated (
	id serial4 NOT NULL,
	reported_by text NULL,
	falls_within text NULL,
	longitude float8 NULL,
	latitude float8 NULL,
	"location" text NULL,
	crime_type text NULL,
	last_outcome_category text NULL,
	"date" text NULL,
	CONSTRAINT london_crime_consolidated_pkey PRIMARY KEY (id)
);