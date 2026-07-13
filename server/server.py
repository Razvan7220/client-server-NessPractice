import socket
import threading


def handle_client(client_socket, client_address):
    """Această funcție rulează pe un thread separat pentru fiecare client."""
    print(f"[THREAD] Pornit pentru {client_address}")
    try:
        # Aici se desfășoară logica cu clientul (de exemplu, meniul)
        data = client_socket.recv(1024).decode('utf-8')
        print(f"[{client_address}]: {data}")

        client_socket.send("Mesaj procesat pe thread separat!\n".encode('utf-8'))
    except Exception as e:
        print(f"Eroare cu clientul {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[THREAD] Închis pentru {client_address}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 1234))
server_socket.listen(5)
print("Serverul MULTI-THREADED rulează și așteaptă clienți...")

try:
    while True:
        client_socket, client_address = server_socket.accept()

        # Creăm un thread nou și îi pasăm funcția și argumentele
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        # Pornim thread-ul (rulează în paralel logica din handle_client)
        client_thread.start()

except KeyboardInterrupt:
    print("\nServerul a fost oprit.")
finally:
    server_socket.close()