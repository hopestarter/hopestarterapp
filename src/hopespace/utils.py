import googlemaps
from django.conf import settings


def geocode(lat, lng):
    """Transforms a coordinate into a location tuple.

    Transforms location coordinates into a  (city,state,country) tuple using
    Google Geocode API.
    """
    client = googlemaps.Client(key=settings.GOOGLE_MAPS_KEY)
    city = state = country = None

    results = client.reverse_geocode((lat, lng))
    addresses = []
    if len(results) > 0:
        for result in results:
            address = [None, None, None]
            for component in result['address_components']:
                if 'country' in component['types']:
                    address[2] = component['long_name']
                if 'administrative_area_level_1' in component['types']:
                    address[1] = component['long_name']
                if 'administrative_area_level_2' in component['types']:
                    address[0] = component['long_name']
            addresses.append(address)
            if len(filter(None, address)) == 3:  # good enough
                break
        city, state, country = addresses[-1]

    return city, state, country
