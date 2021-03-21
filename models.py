"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import datetime, math

class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.

        info is expected to have following keys in the data
            `pdes`   designation of the corresponding NEO
            `name`   name of the NEO, empty if does not exist
            `diameter`  diameter of the NEO 
            `pha`  possibility of the NEO being hazardous

        """
        self.designation = info['pdes']
        self.name = None if len(info['name'])==0 or info['name'] is None else info['name']
        self.diameter = float('nan') if len(info['diameter'])==0 else float(info['diameter'])
        self.hazardous = True if info['pha'] == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = list()

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f'{self.designation} ({self.name})'

    def __str__(self):
        """Return `str(self)`. a human-readable string representation."""
        haz = '' if self.hazardous else 'not'
        return f"A NEO {self.fullname} has a diameter {self.diameter} and is {haz} potentially hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self):
        return {
            'designation':self.designation, 
            'name' : '' if self.name is None else self.name, 
            'diameter_km' : 'NaN' if math.isnan(self.diameter) else self.diameter, 
            'potentially_hazardous' : str(self.hazardous).lower()
        }
    

class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.

    """
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.

        info is expected to have following keys in the data
            `des`   designation of the corresponding NEO
            `cd`    calender date for approach
            `dist`  nominal distance of the NEO from Earth
            `v_rel` velocity of the approach
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # Coerce these values to their appropriate data type and handle any edge cases.
        self._designation = info['des']
        self.time = cd_to_datetime(info['cd'])  
        self.distance = round(float(info['dist']),4)
        self.velocity = round(float(info['v_rel']),4)        
        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """        
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`. Return a human-readable string representation."""
        return f"NEO {self.neo} approaches Earth on {self.time_str} at a distance {self.distance} and velociy {self.velocity}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo})")
    @property
    def designation(self):
        return self._designation

    def serialize(self):
        return {
            'datetime_utc' : self.time_str , 
            'distance_au' : self.distance, 
            'velocity_km_s' : self.velocity
        }


if __name__ == '__main__':
    import csv, json
    with open('data/neos.csv','r') as f:
        reader = csv.DictReader(f)
        data = next(reader)

    neo = NearEarthObject(**data)
    print(neo)


    with open('data/cad.json','r') as f:
        data = json.load(f)

    approach = CloseApproach(**dict(zip(data['fields'], data['data'][0])))
    print(approach)
    