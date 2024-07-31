import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns

# postgres params
dbname = "postgres"
user = "postgres"
password = "123"
host = "localhost"
port = "5432"

try:
    connection = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
    )

    # load data from the table into pandas dataframe
    query = "SELECT * FROM public.london_crime_consolidated"
    df = pd.read_sql_query(query, connection)

finally:
    if connection:
        connection.close()

# extract only year from date
df["year"] = pd.to_datetime(df["date"]).dt.year

# it spotted several rows with errors in the names of neighbourhoods, let's drop them
error_values = ["Error: 404", "Error: 502"]
df_clean = df[~df["neighbourhood"].isin(error_values)]

# aggregating data by neighbourhood, year, and crime_type
aggregated_data = (
    df_clean.groupby(["neighbourhood", "year", "crime_type"])
    .size()
    .reset_index(name="incident_count")
)

# display the full table of aggregated data
# print(aggregated_data.to_string())

# we can save it to .csv or .json and use for analytics and visualizations elsewhere
# aggregated_data.to_csv('london_crime.csv', index=False)

# or visualize with plot
plt.figure(figsize=(14, 7))
sns.lineplot(
    data=aggregated_data, x="year", y="incident_count", hue="neighbourhood", marker="o"
)

plt.title("Crime Incidents by Neighbourhood and Year")
plt.xlabel("Year")
plt.ylabel("Incident Count")
plt.legend(title="Neighbourhood", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()
