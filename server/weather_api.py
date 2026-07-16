import urllib.request
import urllib.parse
import json


def _get_coordinates(location_name):
    """
    Funcție helper (privată) care transformă numele orașului în coordonate (Lat, Lon).
    Returnează (lat, lon, nume_complet) sau (None, None, None) dacă nu găsește.
    """
    # Encodăm numele orașului pentru a fi sigur în URL (ex: spații sau diacritice)
    locatie_url = urllib.parse.quote(location_name)
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={locatie_url}&count=1&language=en&format=json"

    try:
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                return result["latitude"], result["longitude"], f"{result['name']}, {result.get('country', '')}"
    except Exception as e:
        print(f"[API ERROR - Geocoding]: {e}")
    return None, None, None


def fetch_weather(location_name):
    """
    Interfața publică: Primește numele orașului, obține coordonatele,
    cere vremea de la Open-Meteo și returnează un string formatat elegant.
    """
    lat, lon, nume_complet = _get_coordinates(location_name)

    if not lat or not lon:
        return f"Eroare: Nu am putut găsi coordonatele pentru '{location_name}'."

    # URL-ul pentru starea vremii curente (cerem doar temperatura, umiditatea și viteza vântului)
    url_vreme = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"

    try:
        with urllib.request.urlopen(url_vreme, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            current = data["current"]

            temp = current["temperature_2m"]
            umiditate = current["relative_humidity_2m"]
            vant = current["wind_speed_10m"]

            return (
                f"\n=== METEO PENTRU {nume_complet.upper()} ===\n"
                f"• Temperatură:      {temp}°C\n"
                f"• Umiditate aer:    {umiditate}%\n"
                f"• Viteza vântului:  {vant} km/h\n"
            )
    except Exception as e:
        return f"Eroare la obținerea datelor meteo: {e}"
    