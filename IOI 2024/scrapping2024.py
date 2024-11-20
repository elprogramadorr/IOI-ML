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
        return response["result"][0].get("rating", "N/A")
    return "N/A"

def get_ranks_IOI(participant_stats_url):
    """Obtiene los rankings de IOI de un participante por año."""
    soup = get_soup(participant_stats_url)
    rows = soup.select("tr")[2:]
    
    years = list(range(2019, 2025))
    ranks = {year: None for year in years}
    
    for row in rows:
        year = int(row.select('td')[0].text.strip())
        if row.select('td')[11]:
            rank = row.select('td')[11].text.strip()[:-1]  # Remover último carácter (ej: '*')
            ranks[year] = rank
    
    return ranks

def save_to_csv(data, filename="ioi_codeforces.csv"):
    """Guarda los datos en un archivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ["Nombre", "Rating de Codeforces"] + [f"Ranking IOI {year}" for year in range(2019, 2025)]
        writer.writerow(header)
        writer.writerows(data)

def main():
    url = "https://cphof.org/standings/ioi/2024"
    soup = get_soup(url)
    rows = soup.select("table tr")[8:]
    
    data = []
    
    for row in rows:    
        nombre, link, pais = get_participant_data(row)
        stats_link = get_stats_link(link)
        
        if stats_link:
            ranks = get_ranks_IOI(stats_link)
        else:
            ranks = {year: "N/A" for year in range(2019, 2025)}
        
        handle = get_codeforces_handle(link)
        rating = get_codeforces_rating(handle) if handle else "N/A"
        print(nombre, rating, ranks)
        row_data = [nombre, rating] + [ranks[year] for year in range(2019, 2025)]
        data.append(row_data)
    
    save_to_csv(data)
    print("Datos guardados en 'ioi_codeforces.csv'.")

if __name__ == "__main__":
    main()
