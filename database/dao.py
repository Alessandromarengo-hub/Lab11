from database.DB_connect import DBConnect
from model.grafo import Grafo
from model.rifugi import Rifugio


class DAO:
    """
        Implementare tutte le funzioni necessarie a interrogare il database.
        """

    @staticmethod
    def grafo_filtrato(anno):

        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f"""SELECT id, id_rifugio1, id_rifugio2, anno
                    FROM connessione
                    WHERE anno < {anno};
                        """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                graph = Grafo(
                    id = row["id"],
                    id_hub_arrivo=row["id_rifugio1"],
                    id_hub_partenza=row["id_rifugio2"],
                    anno = row["anno"]
                )

                result.append(graph)
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def popola_rifugi():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("❌ Errore di connessione al database.")
            return None

        cursor = cnx.cursor(dictionary=True)
        query = f"""SELECT id, nome, localita,  altitudine, capienza
                            FROM rifugio;
                                """

        try:
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                g = Rifugio(
                    id=row["id"],
                    nome = row["nome"],
                    localita=row["localita"],
                    altitudine=row["altitudine"],
                    capienza=row["capienza"],
                )

                result.append(g)
        except Exception as e:
            print(f"Errore durante la query get_tour: {e}")
            result = None
        finally:
            cursor.close()
            cnx.close()

        return result


    # TODO


