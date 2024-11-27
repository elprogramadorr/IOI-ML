import requests

# def get_participant_count(contest_id):
#     url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&unofficial=false"
#     response = requests.get(url)
#     data = response.json()
    
#     if data['status'] == 'OK':
#         participant_count = data['result']['rows']
#         return len(participant_count)
#     else:
#         return f"Error: {data['comment']}"

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


# contest_id = 2005  # Reemplaza con el contestId que desees
# print(get_participant_count(contest_id))

# print(get_porcentual_rank(2005, 'kkkksc03'))  # Reemplaza con el handle que desees

print(averageLastContest("mickyor"))  # Reemplaza con el handle que desees

# 10 vainas 92

# 5 96
