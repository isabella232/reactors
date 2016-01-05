#!/usr/bin/env python

import agate

def simplify_name(r):
    name = r['Unit Name']

    if '-' not in name:
        return name

    return name.rsplit('-', 1)[0]

def construction_year(r):
    d = r['Construction Date']

    if not d:
        return None

    return d.year

def grid_year(r):
    d = r['Grid Date']

    if not d:
        return None

    return d.year

def shutdown_year(r):
    d = r['Permanent Shutdown Date or LTS Date']

    if not d:
        return None

    return d.year

def main():
    locations = agate.Table.from_csv('locations.csv')

    reactors = agate.Table.from_csv('reactors.csv')

    reactors = reactors.compute([
        ('simple_name', agate.Formula(agate.Text(), simplify_name)),
        ('construction_year', agate.Formula(agate.Number(), construction_year)),
        ('grid_year', agate.Formula(agate.Number(), grid_year)),
        ('shutdown_year', agate.Formula(agate.Number(), shutdown_year))
    ])

    reactors = reactors.join(locations, 'simple_name', 'name')

    print(len(reactors.rows))

    reactors.to_csv('reactors_with_locations.csv')

if __name__ == '__main__':
    main()
