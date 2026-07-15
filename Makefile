# Portul implicit dacă variabila de mediu SERVER_PORT nu este definită
SERVER_PORT ?= 12345

.PHONY: server client run-server run-clients clean

# 1. Construiește serverul (în cazul Python, ne asigurăm că scripturile au permisiuni de execuție)
server:
	@echo "Pregătire aplicație server..."
	chmod +x run-server.sh
	chmod +x server/server.py

# 2. Construiește clientul (ne asigurăm că scripturile au permisiuni)
client:
	@echo "Pregătire aplicație client..."
	chmod +x run-clients.sh
	chmod +x client/client.py

# 3. Rulează serverul folosind run-server.sh și portul din SERVER_PORT
run-server: server
	@echo "Lansare server pe portul $(SERVER_PORT)..."
	./run-server.sh $(SERVER_PORT)

# 4. Rulează cei 100 de clienți în paralel
run-clients: client
	@echo "Lansare 100 de clienți către portul $(SERVER_PORT)..."
	./run-clients.sh $(SERVER_PORT)

# 5. Șterge artefactele de build (folderele temporare __pycache__, fișiere .pyc sau fișiere de test)
clean:
	@echo "Se curăță artefactele de build..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f cod_test.zip
	rm -rf cpp_test

