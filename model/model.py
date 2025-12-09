import networkx as nx
from database.dao import DAO


# Importa Grafo e Rifugio se necessari, ma non sono strettamente usati in questo file
# from model.grafo import Grafo
# from model.rifugi import Rifugio


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self._rifugi_by_id = {}
        # 1. Carica tutti i rifugi dal DB all'avvio
        self._load_rifugi()

    def _load_rifugi(self):
        """Metodo di servizio per caricare la mappa completa ID -> Oggetto Rifugio dal DB."""
        self._rifugi_by_id = {}
        lista_rifugi = DAO.popola_rifugi()
        for r in lista_rifugi:
            self._rifugi_by_id[r.id] = r

    def get_nodes(self):
        """
        ✔️ NECESSARIA PER IL CONTROLLER.
        Restituisce la lista dei nodi (Rifugi) presenti nel grafo costruito.
        Il controller la usa in handle_calcola e _fill_dropdown.
        """
        return list(self.G.nodes)

    def build_graph(self, year: int):
        """
        Costruisce il grafo con i rifugi connessi nell'anno <= year.
        """
        self.G.clear()
        lista_archi = DAO.grafo_filtrato(year)

        for edge in lista_archi:
            # Uso id_hub_arrivo e id_hub_partenza come definito nel tuo DAO
            node_a = self._rifugi_by_id.get(edge.id_rifugio1)
            node_b = self._rifugi_by_id.get(edge.id_rifugio2)

            if node_a and node_b:
                self.G.add_edge(node_a, node_b)

        print(f"Grafo costruito con {len(self.G.nodes)} nodi e {len(self.G.edges)} archi")

    def get_num_neighbors(self, node):
        """
        Risolve l'originale KeyError. Restituisce il grado (numero di vicini).
        Controlla se il nodo è nel grafo (se è stato incluso dall'anno filtrato).
        """
        if node in self.G:
            return self.G.degree[node]
        else:
            # Se il rifugio esiste nel DB ma non è nel grafo filtrato, il grado è 0.
            return 0

    def get_num_connected_components(self):
        """
        Restituisce il numero di componenti connesse.
        """
        return nx.number_connected_components(self.G)

    def get_reachable(self, start):
        """
        Restituisce l'elenco di rifugi raggiungibili da start (escluso start).
        """
        if start not in self.G:
            return []

        # Utilizza la ricerca in ampiezza (BFS) di NetworkX
        tree = nx.bfs_tree(self.G, start)

        # Estrae i nodi raggiunti
        reachable_nodes = list(tree.nodes)

        # Rimuove il nodo di partenza come richiesto dalla traccia
        if start in reachable_nodes:
            reachable_nodes.remove(start)

        return reachable_nodes