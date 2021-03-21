"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
import collections
import keyword

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    neos_collection = []
    with open(neo_csv_path,'r') as f:
        reader = csv.DictReader(f)
        for entry in reader:
            neos_collection.append(
                NearEarthObject(**entry)
            )
    tp = tuple(neos_collection)
    return tp


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    
    with open(cad_json_path,'r') as f:
        data = json.load(f)
    approaches = data['data'] 
    fields = data['fields']
    for n,field in enumerate(fields):
        if keyword.iskeyword(field):
            fields[n] = 'n_' + field

    approaches_collection = []
    for n, appr in enumerate(approaches):        
        approaches_collection.append(
            CloseApproach(**dict(zip(fields, appr)))
        )            
    return tuple(approaches_collection)


if __name__ == '__main__':
    neos = load_neos('data/neos.csv')
    print(neos[5]) 
    approaches = load_approaches('data/cad.json')
    print('\n', approaches[1])
    print('\n', approaches[2])
    

