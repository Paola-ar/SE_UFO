import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "SE_UFO"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.DARK

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Avvistamenti UFO", size=30, weight=ft.FontWeight.BOLD)

        # Riga 1
        self.dd_year = ft.Dropdown(label="Anno", width=200, on_change = self.controller.change_option_year)
        self.dd_shape = ft.Dropdown(label="Forma", width=200)
        self.pulsante_graph = ft.ElevatedButton(text="Crea Grafo", on_click=self.controller.handle_graph)

        row1 = ft.Row([self.dd_year, self.dd_shape, self.pulsante_graph],alignment=ft.MainAxisAlignment.CENTER)
        self.controller.populate_dd()

        self.lista_visualizzazione_1 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # Riga 2
        self.pulsante_path = ft.ElevatedButton(text="Calcola Percorso", on_click=self.controller.handle_path)

        row2 = ft.Row([self.pulsante_path], alignment=ft.MainAxisAlignment.CENTER)
        self.lista_visualizzazione_2 = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

        # --- Toggle Tema ---
        self.toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=self.cambia_tema)

        # --- Layout della pagina ---
        self.page.add(
            self.toggle_cambia_tema,
            self.txt_titolo,
            ft.Divider(),

            row1,
            self.lista_visualizzazione_1,
            ft.Divider(),

            row2,
            self.lista_visualizzazione_2
        )

        self.page.update()

    def cambia_tema(self, e):
        """ Cambia tema scuro/chiaro """
        self.page.theme_mode = ft.ThemeMode.DARK if self.toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        self.toggle_cambia_tema.label = "Tema scuro" if self.toggle_cambia_tema.value else "Tema chiaro"
        self.page.update()
