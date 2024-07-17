import psycopg2
import requests
import time


def get_neighbourhood_name(latitude, longitude):
    url = f"https://data.police.uk/api/locate-neighbourhood?q={latitude},{longitude}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "force" in data and "neighbourhood" in data:
            force = data["force"]
            neighbourhood_id = data["neighbourhood"]

            # fetch neighbourhood details
            neighbourhood_url = f"https://data.police.uk/api/{force}/{neighbourhood_id}"
            neighbourhood_response = requests.get(neighbourhood_url)

            if neighbourhood_response.status_code == 200:
                neighbourhood_data = neighbourhood_response.json()
                return neighbourhood_data.get("name", "Unknown neighbourhood name")
            else:
                return "Could not fetch neighbourhood details"
        else:
            return "Neighbourhood not found for the given coordinates"
    else:
        return f"Error: {response.status_code}"


def update_neighbourhoods():
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123",
            host="localhost",
            port="5432",
        )
        cursor = connection.cursor()

        # get latitude and longitude from table london_crime_consolidated
        cursor.execute(
            "SELECT id, latitude, longitude FROM london_crime_consolidated WHERE neighbourhood IS NULL"
        )
        rows = cursor.fetchall()

        for row in rows:
            row_id, latitude, longitude = row

            # fetch neighbourhood name from API
            neighbourhood_name = get_neighbourhood_name(latitude, longitude)
            print(f"Fetched neighbourhood for ID {row_id}: {neighbourhood_name}")

            # update neighbourhood field in the table
            cursor.execute(
                "UPDATE london_crime_consolidated SET neighbourhood = %s WHERE id = %s",
                (neighbourhood_name, row_id),
            )

            # commit the transaction
            connection.commit()

            # API has limit of 15 calls per second, otherwise it throws http 429 response code (too many requests) and populates it in the table
            time.sleep(1 / 15)

    except Exception as error:
        print(f"Error: {error}")

    finally:
        if connection:
            cursor.close()
            connection.close()


update_neighbourhoods()
