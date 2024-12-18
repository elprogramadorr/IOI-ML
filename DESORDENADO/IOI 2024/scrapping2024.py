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

def get_highest_rated_problem_rating(handle):
    """Obtiene el rating y enlace del problema más difícil resuelto por un usuario."""
    try:
        contests_url = f"https://codeforces.com/api/user.rating?handle={handle}"
        contests_response = requests.get(contests_url).json()
        
        if contests_response["status"] != "OK":
            return None, None
        
        contest_ids = {contest["contestId"] for contest in contests_response["result"]}
        hardest_problem = None

        for contest_id in contest_ids:
            submissions_url = f"https://codeforces.com/api/contest.status?contestId={contest_id}&handle={handle}"
            submissions_response = requests.get(submissions_url).json()
            
            if submissions_response["status"] != "OK":
                continue
            
            submissions = submissions_response["result"]
            
            for submission in submissions:
                if (submission["verdict"] == "OK" and 
                    "problem" in submission and 
                    submission["author"]["participantType"] == "CONTESTANT"):
                    
                    problem = submission["problem"]
                    if "rating" in problem:
                        if not hardest_problem or problem["rating"] > hardest_problem["rating"]:
                            hardest_problem = {
                                "rating": problem["rating"],
                                "link": f"https://codeforces.com/contest/{contest_id}/problem/{problem['index']}"
                            }
        
        if hardest_problem:
            return hardest_problem["rating"], hardest_problem["link"]
        return None, None
    except:
        return None, None

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

def save_to_csv(data, filename="ioi_codeforces_high.csv"):
    """Guarda los datos en un archivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        header = ["Nombre", "Rating de Codeforces", "Problema Más Difícil"] + [f"Ranking IOI {year}" for year in range(2019, 2025)]
        writer.writerow(header)
        writer.writerows(data)

def main():
    url = "https://cphof.org/standings/ioi/2024"
    soup = get_soup(url)
    rows = soup.select("table tr")[8:]
    
    data = []
    
    cant = 0
    for row in rows:    
        cant += 1
        if cant == 3:
            break
        
        nombre, link, pais = get_participant_data(row)
        stats_link = get_stats_link(link)
        
        if stats_link:
            ranks = get_ranks_IOI(stats_link)
        else:
            ranks = {year: "N/A" for year in range(2019, 2025)}
        
        handle = get_codeforces_handle(link)
        if handle:
            rating = get_codeforces_rating(handle)
            highest_problem_rating, _ = get_highest_rated_problem_rating(handle)
        else:
            rating = "N/A"
            highest_problem_rating = "N/A"
        
        print(nombre, rating, highest_problem_rating, ranks)
        row_data = [nombre, rating, highest_problem_rating] + [ranks[year] for year in range(2019, 2025)]
        data.append(row_data)
    
    save_to_csv(data)
    print("Datos guardados en 'ioi_codeforces.csv'.")

if __name__ == "__main__":
    main()
