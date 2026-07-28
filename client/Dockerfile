# 1. Imaginea de bază
FROM python:3.10-slim

# 2. Setăm folderul de lucru în container
WORKDIR /app

# 3. Copiem fișierele necesare (inclusiv arhiva ZIP și modulele)
COPY . .
# 4. Dăm permisiuni de execuție scriptului Bash
RUN chmod +x run-clients.sh

# 5. Comanda de start (parametrul 1 este numele containerului server, parametrul 2 este portul)
CMD ["./run-clients.sh", "server_app", "8080"]