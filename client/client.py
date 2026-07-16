import socket
import sys
from repl_mode import run_repl
from script_mode import run_script_mode  # Importăm noul mod

if len(sys.argv) < 2:
    print("Eroare: Specificați portul! Utilizare:")
    print("  Mod interactiv: python client.py <port>")
    print("  Mod scriptabil: python client.py <port> <command_index> [argumente...]")
    sys.exit(1)

PORT = int(sys.argv[1])
HOST = '127.0.0.1'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))

    # Dacă avem argumente suplimentare, înseamnă că rulăm în mod scriptabil
    # sys.argv[0] este 'client.py', sys.argv[1] este portul, deci de la sys.argv[2] încolo sunt comenzile
    if len(sys.argv) >= 3:
        # Trimitem restul argumentelor către script_mode (de la indexul 2 încolo)
        run_script_mode(client_socket, sys.argv[2:])
    else:
        # Modul interactiv standard (REPL)
        print("✔ Conexiune reușită la server!")
        run_repl(client_socket)

except Exception as e:
    print(f"Eroare conexiune: {e}")
finally:
    client_socket.close()