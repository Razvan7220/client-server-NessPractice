
def run_repl(client_socket):
    while True:
        print("\n--- MENIU COMANDE ---")
        print("1. Afișează Data și Ora")
        print("2. Afișează Informații OS")
        print("3. Consultare Meteo")
        print("4. Încărcare și Compilare Cod ZIP")
        print("5. Ieșire")

        optiune = input("\nIntroduceți indexul comenzii: ").strip()

        if optiune == '5':
            print("Închidere sesiune interactivă...")
            break

        if optiune not in ['1', '2', '3', '4']:
            print("Opțiune invalidă! Încearcă din nou.")
            continue

        # Comunicarea cu serverul
        client_socket.send(optiune.encode('utf-8'))
        raspuns = client_socket.recv(1024).decode('utf-8')

        print(f"\n[Răspuns Server]:\n{raspuns}")
        input("\nApasă Enter pentru a reveni la meniu...")
