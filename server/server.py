import socket
import sys
import threading
from handlers import handle_client

if len(sys.argv) < 2:
    print("Eroare: Specificați portul! Utilizare: python server.py <port>")
    sys.exit(1)

PORT = int(sys.argv[1])
HOST = '127.0.0.1'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Serverul rulează pe portul {PORT}...")

try:
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
except KeyboardInterrupt:
    print("\nServerul a fost oprit.")
finally:
    server_socket.close()
