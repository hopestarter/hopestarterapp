import googlemaps
from django.conf import settings


def geocode(lat, lng):
    """ Transforms a coordinate into a (city,state,country) tuple using Google Geocode API. """
    client = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
    city = state = country = None

    results = client.reverse_geocode((lat, lng))
    if len(results) > 0:
        for component in results[0]['address_components']:
            if 'country' in component['types']:
                country = component['long_name']
            elif 'administrative_area_level_1' in component['types']:
                state = component['long_name']
            elif 'administrative_area_level_2' in component['types']:
                city = component['long_name']

    return city, state, country
