import chess.pgn

def extrahiere_zuege(dateipfad):
    """
    Liest eine PGN-Datei und gibt die Schachzüge für jede Partie als Liste aus.

    Args:
        dateipfad (str): Der Pfad zur PGN-Datei.

    Returns:
        list: Eine Liste von Listen. Jede innere Liste enthält die Züge einer Partie im UCI-Format.
              Gibt eine leere Liste zurück, wenn die Datei nicht gefunden wird oder keine gültigen Partien enthält.
    """
    alle_zuege = []
    try:
        with open(dateipfad) as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break  # Keine weiteren Partien gefunden

                zugliste = [move.uci() for move in game.mainline_moves()]
                alle_zuege.append(zugliste)

    except FileNotFoundError:
        print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    return alle_zuege

if __name__ == "__main__":
    pgn_dateiname = 'testspiel.pgn'  # Ersetze dies durch den Namen deiner PGN-Datei
    partien_zuege = extrahiere_zuege(pgn_dateiname)

    if partien_zuege:
        for i, zuege in enumerate(partien_zuege):
            print(f"Züge für Partie {i+1}:")
            print(zuege)
            print("-" * 20)
    else:
        print("Keine Schachzüge gefunden.")