import requests
import json

# data sources
BASE_URL = "https://data.police.uk/api/crimes-street/all-crime"
NEIGHBOURHOOD_URL = "https://data.police.uk/api/locate-neighbourhood"
FORCE_URL_TEMPLATE = "https://data.police.uk/api/forces/{force}"

# data for one month (April) to analize tendencies year over year, it can be any month. London only.
month = 4
london_lat = 51.5074
london_lng = -0.1278


def get_force_and_neighbourhood(lat, lng):
    response = requests.get(NEIGHBOURHOOD_URL, params={"q": f"{lat},{lng}"})
    if response.status_code == 200:
        data = response.json()
        return data["force"], data["neighbourhood"]
    else:
        raise Exception("Failed to fetch force and neighbourhood")


def get_force_name(force_id):
    response = requests.get(FORCE_URL_TEMPLATE.format(force=force_id))
    if response.status_code == 200:
        data = response.json()
        return data["name"]
    else:
        raise Exception("Failed to fetch force name")


def fetch_london_data(date):
    # parameters for the API call
    params = {"lat": london_lat, "lng": london_lng, "date": date}

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"No data found for date: {date}")
        return None
    else:
        response.raise_for_status()


def extract_relevant_data(records, force_name, date):
    extracted_data = []
    for record in records:
        location = record.get("location", {})
        data = {
            "Reported by": force_name,
            "Falls within": force_name,
            "Longitude": location.get("longitude"),
            "Latitude": location.get("latitude"),
            "Location": location.get("street", {}).get("name"),
            "Crime type": record.get("category"),
            "Last outcome category": (record.get("outcome_status") or {}).get(
                "category"
            ),
            "Date": date,
        }
        extracted_data.append(data)
    return extracted_data


def save_data_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Data saved to {filename}")


def main():
    years = [2022, 2023, 2024]
    force_id, neighbourhood = get_force_and_neighbourhood(london_lat, london_lng)
    force_name = get_force_name(force_id)

    for year in years:
        date = f"{year}-{month:02d}"
        data = fetch_london_data(date)
        if data:
            relevant_data = extract_relevant_data(data, force_name, date)
            json_filename = f"london_crime_data_{year}_{month:02d}.json"
            save_data_to_json(relevant_data, json_filename)


if __name__ == "__main__":
    main()
