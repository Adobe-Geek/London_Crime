london.py - fetches data for London by coordinates, for Aprils 2022, 2023, 2024

dataload.py - loads data into DB into 3 separate tables by each year

SQL scripts consolidate data into 1 table, change data types, create additional empty column with neighbourhoods names

neighbourhoods_names_slow.py - takes coordinates from each row (`16k rows),  finds the neighbourhood name and populates it in the table

load_into_pandas.py - loads consolidated table from database into DataFrame, aggregates by years and neighbourhoods and visualizes results with plotting.
