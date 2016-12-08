"""
TODO:
-   Add other services
-   Add doc
-   Add other objects (Route, RouteLeg, RouteStep)
"""
import requests
from shapely.geometry import Point, shape
import matplotlib.pyplot as plt
import mplleaflet

from .utils import encode_waypoints


class OSRMError(Exception):
    pass


class ValueWarning(Warning):
    pass


class Waypoint:
    def __init__(self, waypoint):
        self.name = waypoint.get('name', None)
        self.distance = waypoint.get('distance', None)
        self.location = waypoint.get('location', None)
        try:
            self.geometry = Point(*self.location)
        except TypeError:
            self.geometry = None


class Route:
    def __init__(self, features, profile='car', **kwargs):

        waypoints = encode_waypoints(features)
        url = 'http://localhost:5000/route/v1/{}/{}'.format(profile, waypoints)

        resp = requests.get(url, params=kwargs)
        json_dict = resp.json()

        if json_dict['code'] != 'Ok':
            raise OSRMError('{}: {}'.format(json_dict['code'],
                                            json_dict.get('message', None)))

        if kwargs.get('alternatives', 'false') == 'true':
            # If multiple routes
            self.distance = [route.get('distance', None) for route in json_dict['routes']]
            self.duration = [route.get('duration', None) for route in json_dict['routes']]
            self.geometry = [shape(route.get('geometry', None)) for route in json_dict['routes']]
            self.routes = json_dict['routes']
        else:
            # If no alternative, then eliminate the single-item list
            br = json_dict['routes'][0]
            self.distance = br.get('distance', None)
            self.duration = br.get('duration', None)
            self.geometry = shape(br['geometry'])
            self.routes = br

        self.waypoints = [Waypoint(wp) for wp in json_dict['waypoints']]
        self.full_json = json_dict

    def show(self):
        fig, ax = plt.subplots()
        ax.plot(*self.geometry.xy)
        mplleaflet.show(fig=fig)

    def __repr__(self):
        return 'Route with a distance of {:.1f} km'.format(self.distance / 1000)


class Nearest:
    pass


class Table:
    pass


class Match:
    pass


class Trip:
    pass


class Tile:
    pass
