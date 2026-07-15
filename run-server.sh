#!/bin/bash

# Verificăm dacă utilizatorul a transmis portul ca parametru ($1)
if [ -z "$1" ]; then
    echo "Eroare: Trebuie să specificați portul ca parametru!"
    echo "Utilizare: ./run-server.sh <PORT>"
    exit 1
fi

PORT=$1

echo "Se pornește serverul pe portul $PORT..."
# Executăm aplicația server în shell-ul curent
# Folosim calea către scriptul tău de server (presupunem că e server/server.py)
python3 server/server.py $PORT