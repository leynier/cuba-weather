#!/usr/bin/env python3

from argparse import ArgumentParser
from json import loads
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import urlopen

__version__ = '0.0.4'

API = 'https://www.redcuba.cu/api/weather_get_summary/{location}'


class RCApiClient:

    def __init__(self, location: str):
        escaped_location = quote(location)
        url = API.format(location=escaped_location)
        response = urlopen(url)
        content = response.read()
        if type(content) == bytes:
            content = content.decode()
        self.data = loads(content)

    @property
    def temperature(self) -> str:
        return self.data['data']['temp']

    @property
    def humidity(self) -> str:
        return self.data['data']['humidity']

    @property
    def pressure(self) -> str:
        return self.data['data']['pressure']

    @property
    def wind(self) -> str:
        return self.data['data']['windstring']

    @property
    def general(self) -> str:
        return self.data['data']['descriptionWeather']


def main():
    parser = ArgumentParser()
    parser.add_argument('location', type=str, help='location name')
    parser.add_argument('-v', '--version', help='show program version', action='store_true')
    parser.add_argument('-t', '--temperature', help='show location temperature', action='store_true')
    parser.add_argument('-u', '--humidity', help='show location humidity', action='store_true')
    parser.add_argument('-p', '--pressure', help='show location pressure', action='store_true')
    parser.add_argument('-w', '--wind', help='show location wind', action='store_true')
    parser.add_argument('-g', '--general', help='show location general information', action='store_true')

    args = parser.parse_args()

    try:
        c = RCApiClient(args.location)
    except HTTPError as ex:
        if ex.code == 404:
            print('Location not found, try checking your orthography or use a near by location.')
        else:
            raise Exception(ex)
        return

    if args.version:
        print(__version__)
    if args.general:
        print(c.general)
    if args.temperature:
        print('Temperature: {temp}°C'.format(temp=c.temperature))
    if args.humidity:
        print('Humidity: {hum}%'.format(hum=c.humidity))
    if args.pressure:
        print('Pressure: {hpa} hpa'.format(hpa=c.pressure))
    if args.wind:
        print('Wind: {wind}'.format(wind=c.wind))

    params = [args.version, args.temperature, args.humidity, args.pressure, args.wind, args.general]
    if args.location and not any(params):
        print(c.general)
        print('Temperature: {temp}°C'.format(temp=c.temperature))
        print('Humidity: {hum}%'.format(hum=c.humidity))
        print('Pressure: {hpa} hpa'.format(hpa=c.pressure))
        print('Wind: {wind}'.format(wind=c.wind))


if __name__ == '__main__':
    main()
