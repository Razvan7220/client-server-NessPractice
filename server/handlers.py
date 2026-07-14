import socket
from services import *


def handle_client(client_socket, client_address):
    print(f"[THREAD] Pornit pentru {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[{client_address} a cerut UC]: {data}")

            if data == '1':
                raspuns = f"Data și Ora Serverului: {get_datetime()}\n"
            elif data == '2':
                raspuns = get_os_info()
            elif data == '3':
                raspuns = "Aici va apărea starea vremii..."
            elif data == '4':
                raspuns = "Aici se va compila codul ZIP..."
            else:
                raspuns = "Comandă necunoscută."

            client_socket.send(raspuns.encode('utf-8'))

    except Exception as e:
        print(f"Eroare cu clientul {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[THREAD] Închis pentru {client_address}")
