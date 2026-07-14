

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

        mesaj_de_trimis = optiune

        # Logica specială pentru Meteo (UC3)
        if optiune == '3':
            oras = input("Introduceți orașul pentru prognoza meteo: ").strip()
            if not oras:
                print("Eroare locală: Numele orașului nu poate fi gol!")
                continue
            mesaj_de_trimis = f"3:{oras}"

        # Comunicarea cu serverul
        client_socket.send(mesaj_de_trimis.encode('utf-8'))
        raspuns = client_socket.recv(4096).decode('utf-8')  # Mărim bufferul la 4096 pentru date mai lungi

        print(f"\n[Răspuns Server]:\n{raspuns}")
        input("\nApasă Enter pentru a reveni la meniu...")
