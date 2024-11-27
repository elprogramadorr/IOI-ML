import pandas as pd
import requests

# Leer el archivo original
data = pd.read_csv('dataset_con_problem.csv')

# Crear una lista para almacenar los datos procesados
processed_data = []

def get_porcentual_rank(contest_id, rank):
    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&unofficial=false"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        participant_count = data['result']['rows']
        
        return (len(participant_count) - rank) / len(participant_count) * 100
    else:
        return f"Error: {data['comment']}"

def averageLastContest(handle):
    if handle == 'N/A' or handle == None:
        return None
    
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url)
    data = response.json()
    n = len(data['result'])
    
    sum = 0
    ind = 0
    cant = 0
    
    while ind<n and cant<10:
        aux = get_porcentual_rank(data['result'][n-1-ind]['contestId'], data['result'][n-1-ind]['rank'])
        if aux != None and type(aux) == float:
            sum += aux
            cant += 1
        ind += 1
        
    return sum / cant


# Procesar cada fila del archivo original
for i in range(len(data)):
    nombre = data.iloc[i]['Nombre']
    handle = data.iloc[i]['Handle de Codeforces']
    rating = data.iloc[i]['Rating de Codeforces']
    ranking_2019 = data.iloc[i]['Ranking IOI 2019']
    ranking_2020 = data.iloc[i]['Ranking IOI 2020']
    ranking_2021 = data.iloc[i]['Ranking IOI 2021']
    ranking_2022 = data.iloc[i]['Ranking IOI 2022']
    ranking_2023 = data.iloc[i]['Ranking IOI 2023']
    ranking_2024 = data.iloc[i]['Ranking IOI 2024']
    rating_problem = data.iloc[i]['Highest Rated Problem']
    average_participation = averageLastContest(handle)
    
    print(rating_problem)
    # Agregar los datos a la lista procesada
    processed_data.append({
        "Nombre": nombre,
        "Handle de Codeforces": handle,
        "Rating de Codeforces": rating,
        "Ranking IOI 2019": ranking_2019,
        "Ranking IOI 2020": ranking_2020,
        "Ranking IOI 2021": ranking_2021,
        "Ranking IOI 2022": ranking_2022,
        "Ranking IOI 2023": ranking_2023,
        "Ranking IOI 2024": ranking_2024,
        "Highest Rated Problem": rating_problem,
        "Average Participation": average_participation
    })
    print(nombre, handle, average_participation)

# Crear un DataFrame con los datos procesados
processed_df = pd.DataFrame(processed_data)

# Exportar el DataFrame a un archivo CSV
processed_df.to_csv('dataset_con_average_participation.csv', index=False)

print("Archivo CSV generado: dataset_procesado.csv")


