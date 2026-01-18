from dataclasses import dataclass,field

@dataclass
class State:
    id : int
    name : str
    capital : str
    lat : float
    lng : float
    area : float
    population : int
    neighbors : list = field(default_factory=list) # quando creo un nuovo oggetto, creo una lista nuova vuota

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.id)
