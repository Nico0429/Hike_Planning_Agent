import requests



def get_co_ordinates(location):
    "This function returns the co-ordinates of the place a user would like to hike"

    base_url = "https://nominatim.openstreetmap.org/search"

    #So we are querying using the location parameter passed from the argument
    query_params = {
        "q": location,
        "format": "json",
        "limit": 1,
    }

    request_headers = {"User-Agent": "s227231201@mandela.ac.za"}
    response = requests.get(base_url, params=query_params, headers=request_headers)

    if response.status_code == 200: #Status code 200 is a good response
        data = response.json()

        if len(data) > 0 :
            first_result = data[0]

            lat = first_result['lat']
            lon = first_result['lon']

            print(lat, lon)
            return lat, lon

        else:
            print(f"Sorry, could not find coordinates for: {location}")
            return None
    else:
        print(f"Server error: {response.status_code}")
        return None