#!/usr/bin/env bash

# Verificăm dacă utilizatorul a transmis HOST-ul și PORT-ul
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Eroare: Trebuie să specificați HOST-ul și PORT-ul!"
    echo "Utilizare: ./run-clients.sh <HOST> <PORT>"
    exit 1
fi

HOST=$1
PORT=$2
ORASE=("Iasi" "Bucuresti" "Cluj" "Timisoara" "Brasov" "Constanta")

echo "Se pornesc 100 de instanțe de clienți către $HOST:$PORT..."

for i in {1..100}
do
    OPTIUNE=$(( ( RANDOM % 4 ) + 1 ))

    if [ "$OPTIUNE" -eq 1 ]; then
        python3 -u client.py $HOST $PORT 1 &

    elif [ "$OPTIUNE" -eq 2 ]; then
        python3 -u client.py $HOST $PORT 2 &

    elif [ "$OPTIUNE" -eq 3 ]; then
        ORAS_ALEATORIU=${ORASE[$RANDOM % ${#ORASE[@]}]}
        python3 -u client.py $HOST $PORT 3 "$ORAS_ALEATORIU" &

    elif [ "$OPTIUNE" -eq 4 ]; then
        python3 -u client.py $HOST $PORT 4 cod_test.zip &
    fi
done

wait

echo "✔ Toți cei 100 de clienți și-au încheiat execuția!"