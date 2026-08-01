import os


def run_script_mode(client_socket, argv):
    """
    Gestionează modul non-interactiv (scriptabil).
    argv conține toate argumentele primite, începând cu indexul comenzii.
    """
    comanda = argv[0]
    # Reconstituim argumentele suplimentare într-un singur string (ex: "Cluj Napoca" sau "cod_test.zip")
    argumente = " ".join(argv[1:]) if len(argv) > 1 else ""

    if comanda in ['1', '2']:
        mesaj = comanda

    elif comanda == '3':
        if not argumente.strip():
            print("Eroare: Trebuie să specifici un oraș! (Ex: python client.py <port> 3 Iasi)")
            return
        mesaj = f"3:{argumente.strip()}"

    elif comanda == '4':
        cale_zip = argumente.strip()
        if not cale_zip or not os.path.exists(cale_zip):
            print(f"Eroare: Fișierul ZIP '{cale_zip}' nu există!")
            return

        # Protocolul de trimitere ZIP
        dimensiune = os.path.getsize(cale_zip)
        client_socket.send(f"4:{dimensiune}".encode('utf-8'))

        # Așteptăm READY de la server
        confirmare = client_socket.recv(1024).decode('utf-8')
        if confirmare != "READY":
            print(f"Serverul a refuzat trimiterea: {confirmare}")
            return

        # Trimitem octeții arhivei
        with open(cale_zip, "rb") as f:
            client_socket.sendall(f.read())

        # Primim răspunsul de la compilare și rulare
        raspuns = client_socket.recv(8192).decode('utf-8')
        print(raspuns)
        return

    else:
        print(f"Eroare: Comandă necunoscută '{comanda}'")
        return

    # Trimiterea și recepția pentru comenzile 1, 2 și 3
    client_socket.send(mesaj.encode('utf-8'))
    raspuns = client_socket.recv(8192).decode('utf-8')
    print(raspuns)
