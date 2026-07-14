from datetime import datetime
from weather_api import fetch_weather
import subprocess

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
        distro = "Debian (detalii indisponibile)"

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
