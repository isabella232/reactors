#!/usr/bin/env python

import agate

def main():
    table = agate.Table.from_csv('reactors_with_locations.csv')

    counts = []

    for year in range(1951, 2015 + 1):
        under_construction = table.where(lambda r: r['construction_year'] <= year and (r['grid_year'] is None or r['grid_year'] > year))

        counts.append([year, len(under_construction.rows)])

    counts = agate.Table(counts)

    counts.to_csv('counts.csv')

if __name__ == '__main__':
    main()
