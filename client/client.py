import socket

# Creează socket-ul TCP al clientului
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 1234))  # Se conectează la server

# Trimite un mesaj către server
mesaj = input("Mesaj: ")
client_socket.send(mesaj.encode('utf-8'))

# Așteaptă răspunsul de la server
raspuns = client_socket.recv(1024).decode('utf-8')
print(f"Răspuns de la server: {raspuns}")

# Închide socket-ul
client_socket.close()