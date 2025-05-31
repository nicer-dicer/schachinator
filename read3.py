import chess
import pgnread2




def square_to_coords(square):
    file = chess.square_file(square) + 1  # 0 = a, ..., 7 = h
    rank = chess.square_rank(square) + 1  # 0 = 1, ..., 7 = 8
    return [file, rank]


def read_loop(zuege, task_queue):
    board = chess.Board()
    white_graveyard_rank = 1
    black_graveyard_rank = 1

    for uci_str in zuege:
        move = chess.Move.from_uci(uci_str)
        from_coords = square_to_coords(move.from_square)
        to_coords = square_to_coords(move.to_square)

        move_type = "normal"
        captured_piece = None

        # Farbe der ziehenden Figur
        mover_color = "W" if board.turn == chess.WHITE else "B"

        if board.is_capture(move):
            move_type = "capture"

            # Wo steht die geschlagene Figur?
            if board.is_en_passant(move):
                capture_square = move.to_square + (-8 if board.turn else 8)
            else:
                capture_square = move.to_square

            captured_piece = board.piece_at(capture_square)

            if captured_piece:
                captured_color = "W" if captured_piece.color == chess.WHITE else "B"

                # Friedhofsziel berechnen
                if captured_piece.color == chess.WHITE:
                    graveyard_coords = [1, white_graveyard_rank]
                    white_graveyard_rank += 1
                else:
                    graveyard_coords = [9, black_graveyard_rank]
                    black_graveyard_rank += 1

                captured_coords = square_to_coords(capture_square)

                # 1️⃣ Geschlagene Figur zum Friedhof
                task_queue.put(captured_coords, False,  captured_color)
                task_queue.put(graveyard_coords, True, captured_color)

                print(f"captured from: {captured_coords + [False, f'captured_{captured_piece.symbol()}', captured_color]}")
                print(f"captured to  : {graveyard_coords + [True, f'captured_{captured_piece.symbol()}', captured_color]}")

        elif board.is_castling(move):
            move_type = "castling"
        elif board.is_en_passant(move):
            move_type = "en_passant"
        elif move.promotion:
            move_type = f"promotion_to_{chess.piece_name(move.promotion)}"

        # 2️⃣ Bewegende Figur mit Farbe
        task_queue.put(from_coords, False, mover_color)
        task_queue.put(to_coords, True, mover_color)

        print(f"from: {from_coords + [False, move_type, mover_color]}")
        print(f"to  : {to_coords + [True, move_type, mover_color]}")

        board.push(move)

    task_queue.put(None)
    
def start_read(task_queue):
    pgn_datei = 'testspiel.pgn'  # Gib hier den Pfad zu deiner PGN-Datei an
    partien_inhalte = pgnread2.lese_pgn_datei_als_string(pgn_datei)  # Verwende pgn_parser

    for inhalt in partien_inhalte:
        zuege = pgnread2.extrahiere_partie_zuege(inhalt)  # Verwende pgn_parser
        if zuege:
            read_loop(zuege, task_queue)  # Rufe read_loop mit den extrahierten Zügen auf
        else:
            print("Keine Züge für diese Partie gefunden.")
    
if __name__ == "__main__":
    task_queue = []
    start_read(task_queue)