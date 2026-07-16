from services import *

def handle_client(client_socket, client_address):
    print(f"[THREAD] Pornit pentru {client_address}")
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            print(f"[{client_address} a cerut UC]: {data}")

            # Desfacem comanda de eventualele argumente.
            # Dacă clientul trimite "3:Iasi", parti[0] va fi "3", iar parti[1] va fi "Iasi".
            parts = data.split(':', 1)
            command = parts[0]
            argument = parts[1] if len(parts) > 1 else ""

            if command == '1':
                raspuns = f"Data și Ora Serverului: {get_datetime()}\n"
            elif command == '2':
                raspuns = get_os_info()
            elif command == '3':
                # Validare pe server: dacă nu s-a trimis locația
                if not argument.strip():
                    raspuns = "Eroare: Trebuie să specifici o locație! (Ex: '3:Iasi')"
                else:
                    raspuns = get_weather_data(argument.strip())
            elif command == '4':
                try:
                    dimensiune_zip = int(argument)
                except ValueError:
                    client_socket.send("Eroare: Dimensiune ZIP invalidă!".encode('utf-8'))
                    continue

                # Pasul 1: Trimitem confirmarea că suntem gata să primim fișierul
                client_socket.send("READY".encode('utf-8'))

                # Pasul 2: Citim exact numărul de bytes specificat
                date_zip = bytearray()
                while len(date_zip) < dimensiune_zip:
                    # Citim în bucăți de maxim 4096 bytes
                    chunk = client_socket.recv(min(4096, dimensiune_zip - len(date_zip)))
                    if not chunk:
                        break
                    date_zip.extend(chunk)

                if len(date_zip) != dimensiune_zip:
                    raspuns = "Eroare: Transmiterea ZIP-ului a fost întreruptă sau incompletă."
                else:
                    # Pasul 3: Trimitem bytes primiți către serviciul de compilare
                    # Importăm funcția compile_and_run_zip din services
                    raspuns = compile_and_run_zip(bytes(date_zip))
            else:
                raspuns = "Comandă necunoscută."

            client_socket.send(raspuns.encode('utf-8'))

    except Exception as e:
        print(f"Eroare cu clientul {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[THREAD] Închis pentru {client_address}")