import socket
import sys
from repl_mode import run_repl
from script_mode import run_script_mode

if len(sys.argv) < 3:
    print("Eroare: Specificați adresa și portul! Utilizare:")
    print("  Mod interactiv: python client.py <host> <port>")
    print("  Mod scriptabil: python client.py <host> <port> <command_index> [argumente...]")
    sys.exit(1)

# MODIFICAREA ESTE AICI (Apar 2 argumente obligatorii acum):
HOST = sys.argv[1]
PORT = int(sys.argv[2])

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    # Deoarece sys.argv[0] e fisierul, sys.argv[1] e host-ul, sys.argv[2] e portul,
    # comenzile efective incep acum de la indexul 3.
    if len(sys.argv) >= 4:
        run_script_mode(client_socket, sys.argv[3:])
    else:
        print(f"✔ Conexiune reușită la serverul {HOST}:{PORT}!")
        run_repl(client_socket)

except Exception as e:
    print(f"Eroare conexiune: {e}")
finally:
    client_socket.close()