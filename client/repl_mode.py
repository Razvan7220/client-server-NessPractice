import socket
import os


def run_repl(client_socket):
    while True:
        print("\n--- MENIU COMENZI ---")
        print("1. Afișează Data și Ora")
        print("2. Afișează Informații OS")
        print("3. Consultare Meteo")
        print("4. Încărcare și Compilare Cod ZIP")
        print("5. Ieșire")

        optiune = input("\nIntroduceți indexul de comandă: ").strip()

        if optiune == '5':
            print("Închidere sesiune interactivă...")
            break

        if optiune not in ['1', '2', '3', '4']:
            print("Opțiune invalidă! Încearcă din nou.")
            continue

        # UC 1 și 2
        if optiune in ['1', '2']:
            client_socket.send(optiune.encode('utf-8'))

        # UC 3 (Meteo)
        elif optiune == '3':
            oras = input("Introduceți orașul pentru prognoza meteo: ").strip()
            if not oras:
                print("Eroare locală: Numele orașului nu poate fi gol!")
                continue
            client_socket.send(f"3:{oras}".encode('utf-8'))

        # UC 4 (Trimitere ZIP)
        elif optiune == '4':
            cale_zip = input("Introduceți calea către arhiva ZIP (ex: cod_test.zip): ").strip()

            if not os.path.exists(cale_zip):
                print(f"Eroare locală: Fișierul '{cale_zip}' nu există!")
                continue

            # Aflăm dimensiunea fișierului în octeți
            dimensiune = os.path.getsize(cale_zip)

            # Pasul A: Trimitem comanda și dimensiunea la server (ex: "4:12450")
            client_socket.send(f"4:{dimensiune}".encode('utf-8'))

            # Așteptăm confirmarea de la server ("OK")
            confirmare = client_socket.recv(1024).decode('utf-8')
            if confirmare != "READY":
                print(f"Serverul a refuzat trimiterea: {confirmare}")
                continue

            # Pasul B: Deschidem ZIP-ul ca bytes și îl trimitem pe tot
            print(f"Se trimite fișierul {cale_zip} ({dimensiune} bytes)...")
            with open(cale_zip, "rb") as f:
                date_binare = f.read()
                client_socket.sendall(date_binare)

        # Așteaptă răspunsul final de la server (rezultatul execuției sau erorile)
        raspuns = client_socket.recv(8192).decode('utf-8')
        print(f"\n[Răspuns Server]:\n{raspuns}")
        input("\nApasă Enter pentru a reveni la meniu...")