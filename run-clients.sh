#!/usr/bin/env bash

# Verificăm dacă utilizatorul a transmis portul
if [ -z "$1" ]; then
    echo "Eroare: Trebuie să specificați portul serverului ca parametru!"
    echo "Utilizare: ./run-clients.sh <PORT>"
    exit 1
fi

PORT=$1
ORASE=("Iasi" "Bucuresti" "Cluj" "Timisoara" "Brasov" "Constanta")

echo "Se pornesc 100 de instanțe de clienți în fundal..."

for i in {1..100}
do
    # 1. Alegem o opțiune aleatorie între 1 și 4
    OPTIUNE=$(( ( RANDOM % 4 ) + 1 ))

    # 2. Lansăm clienții în funcție de opțiunea aleasă
    if [ "$OPTIUNE" -eq 1 ]; then
        # UC1: Data și ora
        python3 client/client.py $PORT 1 > /dev/null &

    elif [ "$OPTIUNE" -eq 2 ]; then
        # UC2: Informații OS
        python3 client/client.py $PORT 2 > /dev/null &

    elif [ "$OPTIUNE" -eq 3 ]; then
        # UC3: Meteo pentru un oraș ales aleatoriu din listă
        ORAS_ALEATORIU=${ORASE[$RANDOM % ${#ORASE[@]}]}
        python3 client/client.py $PORT 3 "$ORAS_ALEATORIU" > /dev/null &

    elif [ "$OPTIUNE" -eq 4 ]; then
        # UC4: Compilare ZIP de test (folosim zip-ul existent)
        python3 client/client.py $PORT 4 cod_test.zip > /dev/null &
    fi
done

# Așteptăm ca toate procesele din fundal pornite de acest script să se termine
wait

echo "✔ Toți cei 100 de clienți și-au încheiat execuția!"