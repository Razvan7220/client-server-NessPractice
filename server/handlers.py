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
            parti = data.split(':', 1)
            comanda = parti[0]
            argument = parti[1] if len(parti) > 1 else ""

            if comanda == '1':
                raspuns = f"Data și Ora Serverului: {get_datetime()}\n"
            elif comanda == '2':
                raspuns = get_os_info()
            elif comanda == '3':
                # Validare pe server: dacă nu s-a trimis locația
                if not argument.strip():
                    raspuns = "Eroare: Trebuie să specifici o locație! (Ex: '3:Iasi')"
                else:
                    raspuns = get_weather_data(argument.strip())
            elif comanda == '4':
                raspuns = "Aici se va compila codul ZIP..."
            else:
                raspuns = "Comandă necunoscută."

            client_socket.send(raspuns.encode('utf-8'))

    except Exception as e:
        print(f"Eroare cu clientul {client_address}: {e}")
    finally:
        client_socket.close()
        print(f"[THREAD] Închis pentru {client_address}")