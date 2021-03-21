"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        # additional auxiliary data structures for faster query 
        self._pdes_to_neos = {}
        self._name_to_neos = {}
        
        # Linking together the NEOs and their close approaches.
        for neo in self._neos:
            self._pdes_to_neos[neo.designation.strip()] = neo
            if neo.name is not None:
                self._name_to_neos[neo.name.strip().upper()] = neo                              
        for appr in self._approaches:            
            try:
                neo = self._pdes_to_neos[appr.designation]
                neo.approaches.append(appr)
                appr.neo = neo                
            except KeyError:
                print(f'NEO des={appr.designation} not found.')

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        designation = designation.strip().upper()
        if designation in self._pdes_to_neos:
            return self._pdes_to_neos[designation]
        return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        name = name.strip().upper()
        if name is not None and len(name)>0:
            try:
                neo = self._name_to_neos[name]
            except KeyError:
                return None
            return neo
        return None

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        for approach in self._approaches:
            match = True
            for f in filters: 
                if not f(approach):
                    match = False
                    break
            if match:
                yield approach

 
                
if __name__ == '__main__':
    from extract import load_approaches, load_neos
    neos = load_neos('data/neos.csv')    
    approaches = load_approaches('data/cad.json')

    neos_db = NEODatabase(neos, approaches)

    designation = '2020 AK3'
    designation = '545274'
    designation = '433'
    print(f"pdes = {designation}\n", neos_db.get_neo_by_designation(designation))

    name = 'Abhramu'
    print(f"name = {name}\n", neos_db.get_neo_by_name(name))
