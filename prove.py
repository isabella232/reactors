#!/usr/bin/env python

import agate

MAPPED_NAMES = {
    'HEYSHAM A': 'HEYSHAM',
    'HEYSHAM B': 'HEYSHAM',
    'SUMMER': 'VIRGIL C. SUMMER',
    'LUNGMEN 1': 'LUNGMEN',
    'LUNGMEN 2': 'LUNGMEN',
    'ROSTOV': 'VOLGODONSK',
    'NOVOVORONEZH 2': 'NOVOVORONEZH',
    'LENINGRAD 2': 'LENINGRAD',
    'AKADEMIK LOMONOSOV': 'PEVEK',
    'SHIN-KORI': 'SHIN-KORI I',
    'PFBR': 'MADRAS',
    'SHIDAO BAY': 'SHIDAOWAN',
    'CHANGJIANG': 'CHANG JIANG',
    'BELARUSIAN': 'Ostrovetskaya',
    'CAREM25': 'ATUCHA-CAREM',
    'HALLAM': 'NEBRASKA',
    'GE VALLECITOS': 'VALLECITOS',
    'FERMI': 'ENRICO FERMI',
    'WINFRITH SGHWR': 'WINFRITH',
    'WINDSCALE AGR': 'WINDSCALE',
    'OLDBURY A': 'OLDBURY',
    'DOUNREAY PFR': 'PFR DOUNREAY',
    'BOHUNICE': 'BOHUNICE A1',
    'DOUNREAY DFR': 'DOUNREAY',
    'BELOYARSK': 'BELOYARSKY',
    'APS': 'APS-1 OBNINSK',
    'THTR': 'THTR-300',
    'MZFR': 'MZFR Karlsruhe',
    'MUELHEIM': 'MUELHEIM-KAERLICH',
    'KNK II': 'KNK',
    'SUPER': 'CREYS-MALVILLE',
    'ST. LAURENT A': 'ST. LAURENT',
    'G': 'MARCOULE',
    'EL': 'MONTS D\'ARREE',
    'CHINON A': 'CHINON',
    'ROLPHTON NPD': 'NPD',
    'ARMENIAN': 'ARMENIA',
    'ROBINSON': 'H.B. ROBINSON',
    'HARRIS': 'SHEARON HARRIS',
    'GINNA': 'R.E. GINNA',
    'COOK': 'DONALD COOK',
    'ANO': 'ARKANSAS ONE',
    'HARTLEPOOL A': 'HARTLEPOOL',
    'HIGASHI DORI': 'HIGASHIDORI',
    'ST. LAURENT B': 'ST. LAURENT',
    'CHOOZ B': 'CHOOZ',
    'CHINON B': 'CHINON',
    'QINSHAN 3': 'QINSHAN',
    'QINSHAN 2': 'QINSHAN',
    'FANGJIASHAN': 'QINSHAN',
    'DAYA BAY': 'GUANGDONG',

}

def simplify_name(r):
    name = r['Unit Name'].strip()

    if '-' in name:
        name = name.rsplit('-', 1)[0].strip()

    if name in MAPPED_NAMES:
        return MAPPED_NAMES[name]

    return name

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
