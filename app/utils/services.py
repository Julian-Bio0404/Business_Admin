"""Third Services."""

# Utilities
import requests


def api_maps(geolocation: str):
    """
    Connection to nominatim geolocation api.
    Determine country, state and city from a geolocation.
    """
    geolocation = geolocation.split(',')
    lat, lng = geolocation[0],  geolocation[1]

    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {'lat': lat, 'lon': lng, 'format': 'jsonv2'}
    response = requests.get(url, params=params)

    try:
        country = response.json()['address']['country']
        state = response.json()['address']['state']
        city = response.json()['address']['city']
    except KeyError:
        return None
    return {'country': country, 'state': state, 'city': city}
