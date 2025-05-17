import chess

# Liste der Züge im UCI-Format
zuege = [
    'e2e4', 'c7c5', 'g1f3', 'a7a6', 'd2d3', 'g7g6', 'g2g3', 'f8g7',
    'f1g2', 'b7b5', 'e1g1', 'c8b7', 'c2c3', 'e7e5', 'a2a3', 'g8e7',
    'b2b4', 'd7d6', 'b1d2', 'e8g8', 'd2b3', 'b8d7', 'c1e3', 'a8c8',
    'a1c1', 'h7h6', 'f3d2', 'f7f5', 'f2f4', 'g8h7', 'd1e2', 'c5b4',
    'a3b4', 'e5f4', 'e3f4', 'c8c3', 'c1c3', 'g7c3', 'f4d6', 'd8b6',
    'd6c5', 'd7c5', 'b4c5', 'b6e6', 'd3d4', 'f8d8', 'e2d3', 'c3d2',
    'b3d2', 'f5e4', 'd2e4', 'e7f5', 'd4d5', 'e6e5', 'g3g4', 'f5e7',
    'f1f7', 'h7g8', 'd3f1', 'e7d5', 'f7b7', 'e5d4', 'g1h1', 'd8f8',
    'f1g1', 'd5e3', 'b7e7', 'a6a5', 'c5c6', 'a5a4', 'g1e3', 'd4e3',
    'e4f6', 'f8f6', 'e7e3', 'f6d6', 'h2h4', 'd6d1', 'h1h2', 'b5b4', 'c6c7'
]

def square_to_coords(square):
    file = chess.square_file(square) +1 # 0 = a, ..., 7 = h
    rank = chess.square_rank(square) +1 # 0 = 1, ..., 7 = 8
    return [file, rank]

def read_loop(task_queue):
    board = chess.Board()
    for uci_str in zuege:
        move = chess.Move.from_uci(uci_str)
        from_coords = square_to_coords(move.from_square)
        to_coords = square_to_coords(move.to_square)

        # Zum Queue hinzufügen
      #  task_queue.put(from_coords + [False])  # von Feld
       # task_queue.put(to_coords + [True])     # zu Feld

        # Zum Debuggen/Überprüfen
        print(f"target_field = {from_coords + [False]}")
        print(f"target_field = {to_coords + [True]}")

        board.push(move)

    # task_queue.put(None)  # Beendet die Schleife
if __name__ == "__main__":
    read_loop("pommes")