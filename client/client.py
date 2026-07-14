import socket
import sys
from repl_mode import run_repl

if len(sys.argv) < 2:
    print("Eroare: Specificați portul! Utilizare: python client.py <port>")
    sys.exit(1)

PORT = int(sys.argv[1])
HOST = '127.0.0.1'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((HOST, PORT))
    print("✔ Conexiune reușită la server!")

    # Lansăm modul REPL din fișierul separat
    run_repl(client_socket)

except Exception as e:
    print(f"Eroare conexiune: {e}")
finally:
    client_socket.close()
