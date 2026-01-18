import flet as ft
from model.model import Model
from UI.view import View

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self._list_year = []
        self._list_shape = []

    def populate_dd(self):
        """ Metodo per popolare i dropdown """
        # TODO
        sighting_list = self._model.list_sighting # prendo lista avvistamenti
        #self._list_shape = sighting_list

        # Popola lista anni unici
        for n in sighting_list:
            if n.s_datetime.year not in self._list_year:
                self._list_year.append(n.s_datetime.year) # può essere anche mese o giorno

        # Popola dropdown anni
        for anno in self._list_year:
            (self._view.dd_year.options.append(ft.dropdown.Option(anno)))

        self._view.update()

    def change_option_year(self,e):
        # handler di dd_year associato all'evento "on_change"
        self._populate_dd_shape()

    def _populate_dd_shape(self):
        # Metodo per popolare il dropdorwn dd_shape con le forme filtrate in base all'anno
        self._list_shape = self._model.get_shapes(self._view.dd_year.value)

        # popola il dropdown shapes
        for shape in self._list_shape:
            self._view.dd_shape.options.append(ft.dropdown.Option(shape))

        self._view.update()


    def handle_graph(self, e):
        """ Handler per gestire creazione del grafo """
        # TODO
        selected_year = self._view.dd_year.value
        selected_shape = self._view.dd_shape.value

        # Pulisce area risultato
        self._view.lista_visualizzazione_1.controls.clear()

        # costruisce grafo con i parametri selezionati
        self._model.build_graph(selected_shape, selected_year)

        # Mostra info grafo
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()}, Numero di archi: {self._model.get_num_of_edges()}"))

        # Mostra somma pesi per nodo
        for node_info in self._model.get_sum_weight_per_node():
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Nodo {node_info[0]}, somma pesi su archi = {node_info[1]}"))

        self._view.update()





    def handle_path(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del cammino """
        # TODO
        self._model.compute_path()

        # pulisce area percorso
        self._view.lista_visualizzazione_2.controls.clear()

        # mostra peso cammino massimo
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Peso cammino massimo: {self._model.sol_best}"))

        # mostra dettagli percorso
        for edge in self._model.path_edge:
            self._view.lista_visualizzazione_2.controls.append(ft.Text(f"{edge[0].id} --> {edge[1].id}: "
                                                                       f"peso {edge[2]}"
                                                                       f"distanza {self._model.get_distance_weight(edge)}"))

            self._view.update()
