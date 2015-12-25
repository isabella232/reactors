#!/usr/bin/env python

from collections import defaultdict
import json

import agate

def main():
    table = agate.Table.from_csv('reactors_with_locations.csv')

    sites = set(table.columns['simple_name'].values())

    output = {
        'sites': {},
        'years': {}
    }

    for site in sites:
        site_row = table.find(lambda r: r['simple_name'] == site)

        if not site_row['lat'] or not site_row['lng']:
            continue

        output['sites'][site] = [float(site_row['lng']), float(site_row['lat'])]

    for year in range(1955, 2016):
        year_sites = {}

        for row in table.rows:
            if row['grid_year'] and row['grid_year'] <= year:
                year_sites[row['simple_name']] += 'operational'

        output['years'][year] = [(k, v) for k, v in year_sites.items()]

    with open('src/data/reactors.json', 'w') as f:
        json.dump(output, f)

if __name__ == '__main__':
    main()
