#!/usr/bin/env python

import agate

def simplify_name(r):
    name = r['Unit Name']

    if '-' not in name:
        return name

    return name.rsplit('-', 1)[0]

def main():
    locations = agate.Table.from_csv('locations.csv')

    reactors = agate.Table.from_csv('reactors.csv')

    reactors = reactors.compute([
        ('simple_name', agate.Formula(agate.Text(), simplify_name))
    ])

    reactors = reactors.join(locations, 'simple_name', 'name')

    print(len(reactors.rows))

    reactors.to_csv('reactors_with_locations.csv')

if __name__ == '__main__':
    main()
