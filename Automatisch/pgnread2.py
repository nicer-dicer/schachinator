import chess.pgn
import io  # Für die Verwendung von StringIO

def extrahiere_partie_zuege(pgn_inhalt):
    """
    Extrahiert die Züge der Hauptvariante aus dem Inhalt einer einzelnen PGN-Partie.

    Args:
        pgn_inhalt (str): Der Inhalt einer einzelnen PGN-Partie als String.

    Returns:
        list: Eine Liste der Züge im UCI-Format.
    """
    try:
        game = chess.pgn.read_game(io.StringIO(pgn_inhalt)) # Verwende StringIO, um String zu lesen
        if game:
            return [move.uci() for move in game.mainline_moves()]
        else:
            return []
    except Exception as e:
        print(f"Fehler beim Parsen der Partie: {e}")
        return []

def lese_pgn_datei_als_string(dateipfad):
    """
    Liest eine PGN-Datei und gibt den Inhalt jeder Partie als Liste von Strings zurück.
    """
    partien = []
    try:
        with open(dateipfad) as f:
            partie = ""
            for line in f:
                partie += line
                if line.strip().endswith("1-0") or line.strip().endswith("0-1") or line.strip().endswith("1/2-1/2") or "*" in line:
                    partien.append(partie)
                    partie = ""
            if partie.strip(): # Letzte Partie ohne Ergebniszeichen
                partien.append(partie)
    except FileNotFoundError:
            print(f"Fehler: Datei '{dateipfad}' nicht gefunden.")
    return partien


if __name__ == "__main__":
    pgn_datei = 'testspiel.pgn'
    partien_inhalte = lese_pgn_datei_als_string(pgn_datei)

    for inhalt in partien_inhalte:
        zuege = extrahiere_partie_zuege(inhalt)
        if zuege:
            print("Züge einer Partie:", zuege) # Zur Demonstration
        else:
            print("Keine Züge für diese Partie gefunden.")