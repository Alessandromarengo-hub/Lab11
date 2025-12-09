class Rifugio:
    def __init__(self, id, nome, localita, altitudine, capienza):
        self.id = id
        self.nome = nome
        self.localita = localita
        self.altitudine = altitudine
        self.capienza = capienza

    def __eq__(self, other):
        if isinstance(other, Rifugio):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"Rifugio({self.id}, {self.nome})"
