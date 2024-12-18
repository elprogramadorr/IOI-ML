import requests
from bs4 import BeautifulSoup
import json
import csv

countries = {
    "China": ["orzdevinwang", "Kubic", "MagicalFlower", "PubabaOnO"],
    "Russia": ["arbuzick", "Qwerty1232", "bashkort", "green_gold_dog"],
    "Japan": ["PCTprobability", "shiomusubi496", "Forested", "hirayuu_cf"],
    "United States of America": ["hyforces", "rainboy", "PurpleCrayon", "GusterGoose27"],
    "Iran": ["ParsaDox", "Dorost", "AmirAli-Asgari", "amirhoseinfar1385"],
    "Poland": ["Adam_GS", "Rafi22", "Jan Gwiazda", "Arapak"],
    "Canada": ["BalintR", "skittles1412", "Trentium", "Mkswll"],
    "Israel": ["elazarkoren", "ItamarNir", "Alon-Tanay", "CommandMaster"],
    "Republic of Korea": ["Mingyu331", "heeew", "mickeyjung", "kes0716"],
    "Vietnam": ["ahihi1234", "socpite", "hotboy2703", "bachbeo2007"],
    "Bulgaria": ["Sedmoklasnikut", "VesselinMarkovich", "libobil", "andreystefanov"],
    "Romania": ["Andrei_ierdnA", "RaresFelix", "valeriu", "anpaio"],
    "India": ["kshitij_sodani", "PoPularPlusPlus", "SmolBrain", "unforgettablepl"],
    "Singapore": ["briX1210", "kymmykym", "TheRaptor0225", "pavement"],
    "Turkey": ["erray", "tolbi", "Weobe", "Nummer_64"],
    "Belarus": ["qilby", "k1r1t0", "topovik", "mechakotik"],
    "Serbia": ["wxhtzdy", "NemanjaSo2005", "prokulijander", "urosk"],
    "Hong Kong": ["bedrockfake", "WongChun1234", "culver0412", "onbert"],
    "Brazil": ["_rey", "LoboLobo", "Lalic", "clarinha"],
    "Taiwan": ["becaido", "PCC", "zacharychao", "LittleOrange666"],
    "United Kingdom": ["Hanksburger", "sammyuri", "Boomyday12343", "anango"],
    "Bangladesh": ["Soumya1", "Jarif_Rahman", "AkibAzmain", "Desh01"],
    "Kazakhstan": ["shenfe1", "MnTm", "Issa", "Tima5"],
    "Ukraine": ["xGaz_", "Ignut", "TheQuantiX", "160cm"],
    "Mongolia": ["Irmuun.Ch", "Onolt_kh", "tamir1", "ezzzay"],
    "Syria": ["edogawa_something", "aminsh", "NeroZein", "Abito"],
    "Hungary": ["gortomi", "Error-42", "Valaki2", "zsombor"],
    "Italy": ["BestCrazyNoob", "franv", "jamesbamber", "AlesL0"],
    "Georgia": ["Phantom_Performer", "DzadzoD", "Nika533", "otarius"],
    "Croatia": ["celin", "DinoHadzic", "ltunjic", "nvujica"],
    "Spain": ["Esomer", "Dalek_of_Rivia", "danx", "Hectorungo_18"],
    "Switzerland": ["42kangaroo", "RecursiveCo", "EliasBauer", "Ursus5805"],
    "Armenia": ["Tsovak", "alex_2008", "c2zi6", "GaGeV"],
    "Azerbaijan": ["fuad720", "Huseyn123", "dmraykhan", "Tahirliyev"],
    "Moldova": ["alinp", "TimDee", "mesanu", "_Vanilla_"],
    "Thailand": ["thawin.ice", "kunzaZa183", "sleepntsheep", "NortGlG"],
    "Kyrgyzstan": ["yanb0", "Alihan_8", "Relice", "Baytoro"],
    "France": ["oscar1f", "raphaelp", "anton6", "anatole4242"],
    "Uzbekistan": ["Sunnatov", "Husanboy", "heaven2808h", "MardonbekHazratov"],
    "Pakistan": ["Ghulam_Junaid", "Muhammad-Saram", "Kaleem_Raza_Syed", "M.UmairAhmadMirza"],
    "Tajikistan": ["outfinity", "MmusoM", "hasan06", "Ansori"],
    "Mexico": ["efishel", "joseandreslemus", "LoganGD", "SopaconK"],
    "North Macedonia": ["Blagoj", "damjandavkovz", "VMaksimoski008", "coolplum"],
    "Czech Republic": ["0npata", "aymanrs", "Tonyl", "honzinsliva", "Trustfulcomic"],
    "Cyprus": ["Theo830", "Trumling", "ALeonidou", "mariza_CY"],
    "Slovakia": ["prvocislo", "viliamgott", "IMackerI", "pritrskypatrik"],
    "Saudi Arabia": ["AverageDiv1Enjoyer", "vahmad", "Essa2006", "Erering"],
    "Palestine": ["Wawi_", "Rushdi", "Abduallah Sherbini", "blushinghentaigirl"],
    "Philippines": ["pwned", "jer033", "ProtonDecay314", "Ausp3x"],
    "Morocco": ["aymanrs", "YassirSalama4", "Medeali", "PotatoTheWarrior2"],
    "Sweden": ["TheodorBeskow", "qwusha", "goben", "slushtre"],
    "Tunisia": ["faresnebili", "MarwenElarbi", "YassineBenYounes", "Friday_night"],
    "Algeria": ["speedcode", "gok_usan", "Chams3927", "DriciHachem"],
    "Cuba": ["CTB220406", "Marco_Escandon", "Maite_Morales", "SN0WM4N"],
    "Jordan": ["Rayo", "TorresianCrow", "samsoom", "Aybak"],
    "Netherlands": ["j_vdd16", "Boas", "Increedible", "2288"],
    "Belgium": ["Nonoze", "Ludissey", "Alban Van Vyve", "Akram Zakine"],
    "Argentina": ["Edu175", "biank", "SpecterByte", "FabriATK"],
    "Turkmenistan": ["stdfloat", "Halym2007", "Champ.", "Hojamuhammet"],
    "Bolivia": ["shezitt", "Gabriel___", "Lincito_31", "aguss"],
    "Germany": ["waipoli", "sim_ba", "Servant_of_the_Lord", "UncreativeDev"],
    "Chile": ["EdL", "TKTO", "FranciscoPinhao", "Bors__"],
    "Ireland": ["pitu", "FionnKimberOShea", "Yuan_Li", "Shuyan Feng"],
    "Colombia": ["MartinezMiners", "oculars_focuses", "Guanexxx", "juan_o_182"],
    "Dominican Republic": ["enderr", "baldwinhuang1", "Adriano4fk", "pierre.rouches"]
}


def lenLongestCommonSubsequence(A, B):
    n = len(A)
    m = len(B)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if A[i - 1] == B[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[n][m]

def getHandle(primerNombre, pais):
    
    if not pais in countries:
        return None
    
    
    # si solo queda uno, retornar ese
    if len(countries[pais]) == 1:
        return countries[pais][0]
    
    for handle in countries[pais]:
        if lenLongestCommonSubsequence(primerNombre, handle) >= 4:
            return handle
        url = f"https://codeforces.com/api/user.info?handles={handle}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["result"][0].get("firstName") and lenLongestCommonSubsequence(primerNombre, data["result"][0]["firstName"]) >= 4:
                return handle
    return None

def save_to_csv(competitors, filename="competitors 2024.1.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escribir encabezados
        writer.writerow(["Name", "Profile URL", "Codeforces Handle"])
        
        # Escribir datos
        for competitor in competitors:
            writer.writerow([competitor.name, competitor.profile_url, competitor.codeforces_url])


class Competitor:
    def __init__(self, name, profile_url, codeforces_url=None):
        self.name = name
        self.profile_url = profile_url
        self.codeforces_url = codeforces_url

    def to_dict(self):
        return {
            "name": self.name,
            "profile_url": self.profile_url,
            "codeforces_url": self.codeforces_url
        }

url = "https://stats.ioinformatics.org/results/2024"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tr")
    competitors = []   
    tienen_cf = 0
    
    cant = 0
    for row in rows:
        cells = row.find_all("td")
        cant += 1
        
        if len(cells) > 1:
            name_cell = cells[1]
            
            link = name_cell.find("a")
            
            if link and "href" in link.attrs:
                name = link.text.strip()
                
                profile_url = f"https://stats.ioinformatics.org/{link['href']}"
                competitor_response = requests.get(profile_url)
                
                print("buscar ", profile_url)
                if competitor_response.status_code == 200:
                    competitor_soup = BeautifulSoup(competitor_response.text, "html.parser")
                    
                    codeforces_link = competitor_soup.find("div", class_="participantinfo")
                    codeforces_link = codeforces_link.find("div", class_="participantdata").find("a")                    
                    pais = cells[2].text.strip()
                    
                    if codeforces_link and "codeforces.com/profile/" in codeforces_link['href']:
                        codeforces_url = codeforces_link['href']
                        handle_cf = codeforces_url.split("/")[-1]
                    else:
                        codeforces_url = None
                        handle_cf = getHandle(name.split()[0], pais)
                    
                    if handle_cf != None and pais in countries and handle_cf in countries[pais]:
                        # eliminar del diccionario
                        countries[pais].remove(handle_cf)
                                
                    competitor = Competitor(name, profile_url, handle_cf)
                    competitors.append(competitor)
                else:
                    print(f"Error al acceder a la página del competidor {name}")
    
    save_to_csv(competitors)  # Guarda los datos en un CSV
    print("Datos guardados en 'competitors.csv'")