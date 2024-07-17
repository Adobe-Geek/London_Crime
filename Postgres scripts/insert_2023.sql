INSERT INTO public.london_crime_consolidated (
    reported_by, 
    falls_within, 
    longitude, 
    latitude, 
    "location", 
    crime_type, 
    last_outcome_category, 
    "date"
)
SELECT 
    reported_by, 
    falls_within, 
    longitude, 
    latitude, 
    "location", 
    crime_type, 
    last_outcome_category, 
    "date"
FROM public.london_crime_data_2023;