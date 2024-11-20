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
    print(stats_link)
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
            print(rank)
    
    return 1


def save_to_csv(data, filename="ioi_codeforces.csv"):
    """Guarda los datos en un archivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Rating de Codeforces"])
        writer.writerows(data)

def main():       
    url = "https://cphof.org/standings/ioi/2024"
    soup = get_soup(url)
    rows = soup.select("table tr")[9:]
    
    print(get_ranks_IOI("https://stats.ioinformatics.org/people/6289"))
    
    exit()
    
    data = []
    
    cant=0
    for row in rows:
        cant += 1
        if cant > 10:
            break
        nombre, link, pais = get_participant_data(row)
        handle = get_codeforces_handle(link)
        rating = get_codeforces_rating(handle) if handle else "N/A"
        link_stats = get_stats_link(link)
        data.append([nombre, rating])
    
    save_to_csv(data)
    print("Datos guardados en 'ioi_codeforces.csv'.")

if __name__ == "__main__":
    main()
