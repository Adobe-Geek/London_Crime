london.py - grabs data for London, for Aprils 2022, 2023, 2024

dataload.py - loads data into DB into 3 separate tables by each year

SQL scripts consolidate data into 1 table, change data types, create additional empty column with neighbourhoods names

neighbourhoods_names_slow.py - takes coordinates from each row (`16k rows),  finds the neighbourhood name and populates it in the table

at this point data is prepared for futher analysis

TO DO NEXT:

pandas part

visualizations with Tableau
