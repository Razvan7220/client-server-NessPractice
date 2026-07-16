from datetime import datetime
from weather_api import fetch_weather
import subprocess
import tempfile
import zipfile
import os

def get_datetime():
    """UC1: Returnează data și ora curentă de pe server."""
    acum = datetime.now()
    return acum.strftime("%Y-%m-%d %H:%M:%S")

def get_os_info():
    """UC2: Rulează comenzi Linux în fundal și adună detaliile despre sistem."""
    try:
        # 1. OS Distro
        # lsb_release -d returnează "Description: Debian GNU/Linux 13 (trixie)"
        # Folosim .split(":") pentru a păstra doar ce este după "Description:"
        distro_raw = subprocess.check_output("lsb_release -d", shell=True).decode('utf-8')
        distro = distro_raw.split("Description:")[1].strip()
    except Exception:
        distro = "Linux (detalii indisponibile)"

    try:
        # 2. Uptime
        uptime = subprocess.check_output("uptime -p", shell=True).decode('utf-8').strip()
    except Exception:
        uptime = "Indisponibil"

    try:
        # 3. CPU Type
        # shell=True este obligatoriu aici pentru a permite folosirea conductelor (|) din Linux
        cpu_raw = subprocess.check_output("cat /proc/cpuinfo | grep 'model name' | uniq", shell=True).decode('utf-8')
        cpu = cpu_raw.split(":")[1].strip()
    except Exception:
        cpu = "Indisponibil"

    try:
        # 4. Available Memory
        free_raw = subprocess.check_output("free -h", shell=True).decode('utf-8')
        lines = free_raw.splitlines()
        # lines[1] este rândul "Mem:  30Gi  6.2Gi  18Gi  79Mi  6.2Gi  24Gi"
        mem_data = lines[1].split()
        total_mem = mem_data[1]      # A doua coloană
        available_mem = mem_data[6]  # A șaptea coloană (index 6)
        memory = f"Total: {total_mem} | Disponibil: {available_mem}"
    except Exception:
        memory = "Indisponibilă"

    # Formătăm totul într-un singur string elegant
    return (
        f"\n=== DETALII SISTEM (SERVER) ===\n"
        f"• Distribuție OS: {distro}\n"
        f"• Uptime:         {uptime}\n"
        f"• Procesor:       {cpu}\n"
        f"• Memorie RAM:    {memory}\n"
    )

def get_weather_data(location):
    """UC3: Apelează API-ul extern pentru a lua datele meteo ale unei locații."""
    if not location:
        return "Eroare: Locația trimisă este goală!"
    return fetch_weather(location)


def compile_and_run_zip(zip_bytes):
    """UC4: Salvează zip-ul în RAM/disc temporar, dezarhivează, compilează și rulează."""
    # Creăm un director temporar izolat în sistemul Linux
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "archive.zip")

        # Salvăm octeții primiți în fișierul zip temporar
        with open(zip_path, "wb") as f:
            f.write(zip_bytes)

        try:
            # Dezarhivăm conținutul direct în folderul temporar
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        except Exception as e:
            return f"Eroare la dezarhivare: {e}"

        # Ștergem arhiva zip acum, ca să nu încurce compilatorul la căutarea fișierelor
        os.remove(zip_path)

        # Căutăm fișierele .cpp din folderul temporar
        cpp_files = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if f.endswith('.cpp')]
        if not cpp_files:
            return "Eroare: Nu s-a găsit niciun fișier .cpp în rădăcina arhivei ZIP!"

        output_binary = os.path.join(temp_dir, "program_binar")

        # --- COMPILAREA ---
        # Construim comanda de compilare: g++ main.cpp helper.cpp -o program_binar
        comanda_compilare = ["g++"] + cpp_files + ["-o", output_binary]

        rezultat_compilare = subprocess.run(
            comanda_compilare,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Dacă codul de retur nu e 0, înseamnă că avem erori de compilare
        if rezultat_compilare.returncode != 0:
            return f"=== EROARE DE COMPILARE ===\n{rezultat_compilare.stderr}"

        # --- EXECUTAREA ---
        try:
            # Rulăm binarul proaspăt compilat
            rezultat_executie = subprocess.run(
                [output_binary],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5  # Timeout de securitate să nu ruleze la infinit
            )

            # Returnăm ce a printat programul C++ în consolă
            return (
                f"=== COMPILARE REUȘITĂ ===\n"
                f"--- Rezultat Execuție: ---\n"
                f"{rezultat_executie.stdout}"
            )

        except subprocess.TimeoutExpired:
            return "Eroare: Execuția programului a depășit limita de 5 secunde (posibil loop infinit)."
        except Exception as e:
            return f"Eroare la rularea binarului: {e}"
