import chess # type: ignore
import pgnread2  # Importiere das pgn_parser Modul

def square_to_coords(square):
    file = chess.square_file(square) + 1  # 0 = a, ..., 7 = h
    rank = chess.square_rank(square) + 1  # 0 = 1, ..., 7 = 8
    return [file, rank]

def read_loop(zuege):  # Übergib die Züge als Argument
    board = chess.Board()
    for uci_str in zuege:
        try:
            move = chess.Move.from_uci(uci_str)
            if move in board.legal_moves:
                from_coords = square_to_coords(move.from_square)
                to_coords = square_to_coords(move.to_square)

                # Zum Debuggen/Überprüfen
                print(f"target_field = {from_coords + [False]}")
                print(f"target_field = {to_coords + [True]}")

                board.push(move)
            else:
                print(f"Ungültiger Zug: {uci_str} im Kontext des aktuellen Bretts")
        except ValueError:
            print(f"Ungültiger Zug-String: {uci_str}")

if __name__ == "__main__":
    pgn_datei = 'testspiel.pgn'  # Gib hier den Pfad zu deiner PGN-Datei an
    partien_inhalte = pgnread2.lese_pgn_datei_als_string(pgn_datei)  # Verwende pgn_parser

    for inhalt in partien_inhalte:
        zuege = pgnread2.extrahiere_partie_zuege(inhalt)  # Verwende pgn_parser
        if zuege:
            read_loop(zuege)  # Rufe read_loop mit den extrahierten Zügen auf
        else:
            print("Keine Züge für diese Partie gefunden.")