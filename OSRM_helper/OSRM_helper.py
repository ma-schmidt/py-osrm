import requests
from shapely.geometry import shape, Point, LineString
import mplleaflet
import matplotlib.pyplot as plt

class OSRMError(Exception):
    pass

class ValueWarning(Warning):
    pass

class Waypoint:
    def __init__(self, waypoint):
        self.distance = waypoint.get('distance', None)
        self.xy = waypoint.get('location', None)
        self.name = waypoint.get('name', None)
        self.geometry = Point(*self.xy)


class NearestResult:
    def __init__(self, json_dict):
        if json_dict['code'] != 'Ok':
            raise OSRMError('{}: {}'.format(json_dict['code'],
                                            json_dict.get('message', None)))


class Route:
    def __init__(self, points=[], origin=None, destination=None, detailed=True):
        if len(points) > 0:
            if (origin is not None) or (destination is not None):
                raise ValueWarning('When points is set, origin and destination'
                                   'are ignored.')

        elif (origin is not None) and (destination is not None):
            points = []
            if isinstance(origin, Point):
                points.append(origin.xy)
            else:
                points.append(origin)

            if isinstance(destination, Point):
                points.append(destination.xy)
            else:
                points.append(destination)

        else :
            raise ValueError('Need either a list of points or an origin'
                             'and a destination')


        coord_url = ';'.join(['{},{}'.format(x, y) for x, y in points])
        base_url = 'http://localhost:5000/route/v1/car/'
        url = base_url + coord_url
        payload = {'geometries': 'geojson', 'steps': 'true'}
        if detailed:
            payload['overview'] = 'full'

        resp = requests.get(url, params=payload)
        json_dict = resp.json()

        if json_dict['code'] != 'Ok':
            raise OSRMError('{}: {}'.format(json_dict['code'],
                                            json_dict.get('message', None)))

        route = json_dict.get('routes')[0]

        self.distance = route.get('distance', None)
        self.duration = route.get('duration', None)
        self.geometry = LineString(json_dict['routes'][0]['geometry']['coordinates'])
        self.origin = Waypoint(json_dict['waypoints'][0])
        self.destination = Waypoint(json_dict['waypoints'][1])

    def __repr__(self):
        return 'Route with a distance of {:.1f} km'.format(self.distance/1000)

    def show(self):
        fig, ax = plt.subplots()
        ax.plot(*self.geometry.xy)
        mplleaflet.show(fig=fig)
