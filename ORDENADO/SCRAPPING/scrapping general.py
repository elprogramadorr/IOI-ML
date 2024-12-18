import requests
from bs4 import BeautifulSoup
import csv

def get_soup(url):
    """Obtiene y parsea la página HTML."""
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")

def get_participant_data(row):
    """Extrae datos de un participante desde una fila HTML."""
    if row.select("td")[1].select("a"):
        pais = row.select("td")[1].select("a")[1].text.strip()
        link = row.select("a")[2]["href"]
        nombre = row.select("a")[2].text.strip()
    else:
        pais = "Russia"
        link = row.select("a")[0]["href"]
        nombre = row.select("a")[0].text.strip()
            
    return nombre, "https://cphof.org" + link, pais

def get_stats_link(participant_url):
    """Obtiene el link de la página de estadísticas de un participante."""
    soup = get_soup(participant_url)
    stats_link = soup.find('a', href=lambda href: href and href.startswith("http://stats"))
    return stats_link["href"] if stats_link else None

def get_codeforces_handle(participant_url):
    """Obtiene el handle de Codeforces si está disponible."""
    soup = get_soup(participant_url)
    cf_link = soup.find('a', href=lambda href: href and href.startswith("https://codeforces.com/profile"))
    return cf_link["href"].split("/")[-1] if cf_link else None

def get_codeforces_rating(handle):
    """Obtiene el rating de un usuario de Codeforces dado su handle."""
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url).json()
    
    if response.get("status") == "OK":
        return response["result"][0]["rating"]
    return "N/A"

def get_ranks_IOI(participant_url):
    """Obtiene el rango de un participante en la IOI."""
    soup = get_soup(participant_url)
    rows = soup.select("tr")[2:]
    rank = rows[0].select('td')[11].text.strip()
    
    for row in rows:
        if row.select('td')[11]:
            rank = row.select('td')[11].text.strip()
    
    return rank

def read_and_modify_csv(input_filename, output_filename="nuevo_completo.csv"):
    """Lee el CSV original, agrega la columna Pais y guarda el nuevo CSV."""
    with open(input_filename, mode="r", newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        rows = list(reader)
        
        # Añadir la nueva columna "Pais" con valores vacíos
        for row in rows:
            row["Pais"] = ""
        
        # Llenar la columna "Pais" con los valores obtenidos por scraping
        url = "https://cphof.org/standings/ioi/2024"
        soup = get_soup(url)
        table_rows = soup.select("table tr")[8:]
        
        # Asumir que la cantidad de participantes en la tabla de scraping es igual a la cantidad de filas en el CSV
        for i, row in enumerate(table_rows):
            _, _, pais = get_participant_data(row)
            rows[i]["Pais"] = pais
        
        # Guardar el CSV con la nueva columna "Pais"
        with open(output_filename, mode="w", newline="", encoding="utf-8") as outfile:
            fieldnames = reader.fieldnames + ["Pais"]
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

def main():
    # Llamada a la función para leer el CSV original y añadir la columna "Pais"
    read_and_modify_csv("dataset_original.csv")

if __name__ == "__main__":
    main()
