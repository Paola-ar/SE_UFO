from dataclasses import dataclass, field
from datetime import datetime


@ dataclass
class Sighting:
    id : int
    s_datetime : datetime
    city : str
    state : str
    country : str
    shape : str
    duration : int
    duration_hm : str
    comments : str
    date_posted : datetime
    latitude : float
    longitude : float

    def __str__(self):
        return self.country

    def __repr__(self):
        return self.country

    def __hash__(self):
        return hash(self.id)
