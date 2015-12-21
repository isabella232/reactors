#!/usr/bin/env python

"""
These location strings were acquired from https://www.iaea.org/PRIS/home.aspx
by running the following command in the terminal after selecting each year:

SetMarkers.toSource()
"""

import html
import json

import csvkit as csv

FIRST_YEAR = 1951
LAST_YEAR = 2015

def main():
    with open('location_strings.json') as f:
        data = json.load(f)

    locations = {}

    for year in range(FIRST_YEAR, LAST_YEAR + 1):
        s = data[str(year)]

        if not s:
            continue

        s = s.lstrip('function SetMarkers(){').rstrip('}')
        s = html.unescape(s)

        markers = s.split(';')

        for marker in markers[:-1]:
            marker = marker.lstrip('AddMarker(').rstrip(')')
            bits = marker.split(',')

            print(bits)

            lat, lng, name = map(str.strip, bits)
            name = name.strip('\'')

            locations[name] = (lat, lng)

    with open('locations.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'lat', 'lng'])

        for name, (lat, lng) in locations.items():
            writer.writerow([name, lat, lng])

if __name__ == '__main__':
    main()
