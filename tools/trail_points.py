import requests


def get_trail_points(latitude: float, longitude: float, radius: int = 1000):
    """
    Finds hiking trail start and end points within a radius of a given coordinate.

    :param latitude: Latitude of the search area.
    :param longitude: Longitude of the search area.
    :param radius: Search radius in meters (Default is 1000).
    """
    overpass_url = "https://overpass-api.de/api/interpreter"


    overpass_query = f"""
    [out:json];
    (
      way["highway"~"path|footway|track"]["hiking"!="no"](around:{radius},{latitude},{longitude});
      relation["route"="hiking"](around:{radius},{latitude},{longitude});
    );
    out body;
    >;
    out skel qt;
    """

    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        data = response.json()
        elements = data.get('elements', [])

        trails = []
        # Filter for 'way' elements which represent the actual paths
        ways = [e for e in elements if e['type'] == 'way']

        for way in ways:

            name = way.get('tags', {}).get('name')

            if name and name.strip() != "":
                nodes = way.get('nodes', [])
                if len(nodes) >= 2:
                    start_node = nodes[0]
                    end_node = nodes[-1]

                    # Find coordinates for these nodes
                    start_coords = next((e for e in elements if e['id'] == start_node), None)
                    end_coords = next((e for e in elements if e['id'] == end_node), None)

                    if start_coords and end_coords:
                        trails.append({
                            "name": name,
                            "start": (start_coords['lat'], start_coords['lon']),
                            "end": (end_coords['lat'], end_coords['lon'])
                        })

        if trails:
            # Limit the results to prevent the model from getting overwhelmed
            trails = trails[:10]

            output = "I found these named trails nearby. Please ask the user to choose one:\n"
            for i, t in enumerate(trails, 1):
                output += f"{i}. {t['name']}\n"

            # Crucial: The model now only sees names, not bulky coordinate data
            return output
        else:
            return "I couldn't find any named trails in this area. Would you like to try a different location?"