import requests
import atexit
from time import sleep
from geographiclib.geodesic import Geodesic

from ext.pickler import Pickler as pcl
from Cache.cache import cords

geod = Geodesic.WGS84  # define the WGS84 ellipsoid


class GetDistance:
    def __init__(self, app_id='', app_code=''):
        self.app_id = app_id
        self.app_code = app_code
        self.count = 0
        self.__lru = cords

        atexit.register(self.cleanup)

    def calc_distance(self, coord1, coord2):
        try:
            g = geod.Inverse(*coord1, *coord2)
        except Exception as e:
            return 10000000000000000000

        return g['s12'] / 1000

    def get_coord(self, location, tmp_rec=0):
        if tmp_rec == 3:
            print('Error connection')
            return None
        if not isinstance(location, str):
            return
        location = 'Россия,' + ' ' + location.lower()
        if location not in self.__lru.keys():
            api_key = '3XNMb9DRSZDSHDzGNsMlVZZChOsEAFn5QSFuc-xSPsw'
            url = f'https://geocoder.ls.hereapi.com/6.2/geocode.json?apiKey={api_key}&searchtext={location}'
            self.count += 1
            get = requests.get(url, verify=False)
            if get.status_code == 200:
                pcl.dump_pickle_file(get.json(), 'tmp')
                get = get.json()['Response']['View']
                if not get:
                    print('Error location')
                    self.__lru.update({location: None})
                    return None

                coord = tuple(get[0]['Result'][0]['Location']['DisplayPosition'].values())
                self.__lru.update({location: coord})
                return coord
            else:
                sleep(3)
                return self.get_coord(location, tmp_rec + 1)
        else:
            # print('Юзаем кэш')
            return self.__lru[location]

    def num_connection(self):
        return self.count

    def cleanup(self):
        pcl.dump_pickle_file(self.__lru, 'Cache/files/coords.pickle')

    def get_distance(self, city_one, city_two):
        if None in (city_one, city_two):
            return None
        coord_city_one = self.get_coord(city_one)

        coord_city_two = self.get_coord(city_two)

        return self.calc_distance(coord_city_one, coord_city_two)

