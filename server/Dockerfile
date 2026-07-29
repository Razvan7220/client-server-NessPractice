# 1. Imaginea de bază
FROM python:3.10-slim

# 2. Instalăm gcc pentru UC4 (compilarea de cod)
RUN apt update && apt install -y gcc procps lsb-release

# 3. Setăm folderul de lucru în container
WORKDIR /app

# 4. Copiem scripturile și modulele (inclusiv handlers.py)
COPY . .

# 5. Dăm permisiuni de execuție scriptului Bash
RUN chmod +x run-server.sh

# 6. Comanda de start
CMD ["./run-server.sh", "8080"]
