import chess # type: ignore

def square_to_coords(square):
    """
    Wandelt ein Schachfeld (z.B. chess.A1) in ein [Datei, Reihe]-Koordinatenpaar um.
    Dateien (Spalten) sind 1-8 (a=1, h=8), Reihen sind 1-8.
    """
    file = chess.square_file(square) + 1  # 0=a -> 1, ..., 7=h -> 8
    rank = chess.square_rank(square) + 1  # 0=1 -> 1, ..., 7=8 -> 8
    return [file, rank]

def get_field_input(prompt_message):
    """
    Fordert den Benutzer auf, ein Schachfeld einzugeben (z.B. A1, E4).
    Validiert die Eingabe und konvertiert sie in Kleinbuchstaben.
    """
    while True:
        user_input = input(prompt_message).strip() # Leerzeichen am Anfang/Ende entfernen
        
        if user_input.lower() == 'exit':
            return None
        
        try:
            # chess.parse_square erwartet Kleinbuchstaben für Felder wie 'a1', 'e2'.
            # Wir konvertieren hier explizit zu Kleinbuchstaben.
            chess.parse_square(user_input.lower()) 
            return user_input.lower() # Rückgabe des validierten Feldnamens in Kleinbuchstaben
        except ValueError:
            print(f"Fehler: Ungültiges Feldformat '{user_input}'. Bitte gib ein gültiges Schachfeld ein (z.B. E2, G1).")
        except Exception as e:
            print(f"Ein unerwarteter Fehler bei der Eingabeverarbeitung: {e}")

def manual_robot_move_control():
    """
    Ermöglicht die manuelle Eingabe von Start- und Endfeldern
    und simuliert die Roboterbewegung mit Magnetsteuerung.
    """
    print("--- Manuelle Roboter-Schachfiguren-Bewegung ---")
    print("Gib Start- und Zielfelder ein, um Figuren zu bewegen.")
    print("Gib 'exit' ein, um das Programm zu beenden.")

    while True:
        start_field_str = get_field_input("Gib das STARTFELD ein (z.B. E2): ")
        if start_field_str is None: # Benutzer hat 'exit' eingegeben
            break

        end_field_str = get_field_input("Gib das ZIELFELD ein (z.B. E4): ")
        if end_field_str is None: # Benutzer hat 'exit' eingegeben
            break

        try:
            # Umwandlung der Feld-Strings in die internen chess.Square-Indizes
            start_square = chess.parse_square(start_field_str)
            end_square = chess.parse_square(end_field_str)

            # Umwandlung der Square-Indizes in deine [Datei, Reihe]-Koordinaten
            from_coords = square_to_coords(start_square)
            to_coords = square_to_coords(end_square)

            # Ausgabe im gewünschten Format für den Roboter, ohne zusätzliche Texte
            print(f"target_field = {from_coords + [False]}") # [Datei, Reihe, False]
            print(f"target_field = {to_coords + [True]}")     # [Datei, Reihe, True]

            # Hier würde die tatsächliche Kommunikation mit dem Roboter erfolgen.
            
            print("\n-------------------------------------------")

        except ValueError as e:
            print(f"Fehler bei der Feldkonvertierung: {e}. Bitte gib gültige Schachfelder ein.")
        except Exception as e:
            print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

    print("Programm beendet.")

if __name__ == "__main__":
    manual_robot_move_control()