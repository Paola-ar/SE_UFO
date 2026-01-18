import threading

from geopy import distance

from database.dao import DAO
import networkx as nx





class Model:
    def __init__(self):
        self.list_sighting = []
        self.list_shapes = []
        self.list_states = []

        self.G = nx.Graph()
        self._nodes = []
        self._edges = []
        self.id_map = {} # mappa serve per identificare i nodi
        self.sol_best = 0

        self.path = []
        self.path_edge = []

        self.load_sighting()
        #self.load_shapes()
        self.load_states()

    def load_sighting(self):
        self.list_sighting = DAO.get_all_sighting()

    # def load_shapes(self):
    #     self.list_shapes = DAO.get_all_shapes()
    def get_shapes(self,selected_year):
        return DAO.get_all_shapes(selected_year)

    def load_states(self):
        self.list_states = DAO.get_all_state()

    def build_graph(self, s, a):
        self.G.clear()
        print (self.G)
        print (a,s)

        for p in self.list_states:
            self._nodes.append(p) # lista temporanea

        self.G.add_nodes_from(self._nodes)
        self.id_map = {}
        for n in self._nodes:
            self.id_map[n.id] = n # a ogni id del nodo associo il nodo stesso, come chiave l'id e valore il nodo corrispondente

        # ho ottenuto archi, stato uno e due i nodi, e n il peso
        tmp_edges = DAO.get_all_weighted_neigh(a,s)

        self._edges.clear()
        for e in tmp_edges:
            self._edges.append((self.id_map[e[0]], self.id_map[e[1]],e[2])) # l'oggetto stato me lo prendo dalla mappa con l'id

        self.G.add_weighted_edges_from(self._edges)

        #threading.Thread(target=self.mostra_grafo).start() # per visualizzare

    def get_sum_weight_per_node(self):
        pp = []
        for n in self.G.nodes():
            sum_w = 0
            for e in self.G.edges(n,data=True):
                sum_w += e[2]["weight"] # mi prendo il loro peso
            pp.append((n.id,sum_w )) # appendo nodo id corrispondente alla somma di tutti archi di quello specifico nodo

        return pp


    def compute_path(self):
        self.path = [] # lista di default di nodi
        self.path_edge = [] # lista di default di edges # le due sono versioni ottimali
        self.sol_best = 0

        partial = []
        for n in self.get_nodes():
            partial.clear() # esploro tutte le possibili soluzioni partendo dai possibili nodi
            partial.append(n)
            self._ricorsione(partial,[]) # nodo iniziale (partial)

    def _ricorsione(self,partial,partial_edge):
        n_last = partial[-1] # prendo ultimo nodo o primo se è la prima volta

        # verifico tutti i possibili vicini
        neighbors = self.get_admissible_neighbs(n_last, partial_edge) # devo poter analizzare tutte le possibili strade da quel punto di partenza

        # quando ho esplorato tutti i vicini di un determinato nodo di partenza
        if len(neighbors) == 0:
            # devo calcolarmi il peso
            weight_path = self.compute_weight_path(partial_edge)
            if weight_path > self.sol_best: # se è la soluzione migliore, cosi viene settato
                self.sol_best = weight_path + 0.0
                self.path = partial[:]
                self.path_edge = partial_edge[:]
            return


        for n in neighbors: # da tutti i nodi di possibili vicini, esploro tutte le possibili alternative
            # lista di tutti hli edges che sto andando ad esplorare
            partial_edge.append((n_last,n,self.G.get_edge_data(n_last,n)["weight"])) # aggiungo edges: nodo partenza, nodo arrivo e rispettivo peso
            # lista di tutti i nodi che sto andando ad esplorare
            partial.append(n)

            self._ricorsione(partial,partial_edge) #partial avra nodo di partenza e altro nodo successivo; edges avra l'arco che ho settato

            partial.pop()
            partial_edge.pop()




    def get_admissible_neighbs(self, n_last, partial_edges): # nodo da cui sto partendo, e quelli che ho gia visitato nella ricorsione
        all_neigh = self.G.edges(n_last, data=True) # tutti i vicini legati al nodo di partenza
        result = []
        for e in all_neigh:
            if len(partial_edges) != 0:
                if e[2]["weight"] > partial_edges[-1][2]: # peso dell'arco è superiore?
                    result.append(e[1]) # se ok, lo aggiungo come possibile vicino da visitare
            else: result.append(e[1]) # se sono allinizio
        return result

    def compute_weight_path(self,mylist):
        weight = 0
        for e in mylist:
            #sommo tutta la distanza tra i vari stati all'interno della mia lista di nodi
            weight +=  distance.geodesic((e[0].lat,e[0].lng),(e[1].lat,e[1].lng)).km
        return weight

    def get_distance_weight(self,e):
        return distance.geodesic((e[0].lat,e[0].lng),(e[1].lat,e[1].lng)).km





    def get_nodes(self):
        return self.G.nodes()
    def get_edges(self):
        return list(self.G.edges(data=True))

    def get_num_of_nodes(self):
        return self.G.number_of_nodes()
    def get_num_of_edges(self):
        return self.G.number_of_edges()