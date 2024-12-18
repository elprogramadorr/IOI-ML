import pandas as pd


def get_porcentual_rank(contest_id, handle):
    url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&handle={handle}&unofficial=false"
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        participant_count = data['result']['rows']
        
        # print(len(participant_count))
        for i in range(len(participant_count)):
            if participant_count[i]['party']['members'][0]['handle'] == handle:
                rank = participant_count[i]['rank']
                total = len(participant_count)
                return (total - rank) / total * 100
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
    
    for i in range(10):
        ind = n - i - 1
        if ind < 0:
            break
        sum += float(get_porcentual_rank(data['result'][ind]['contestId'], handle))
    return sum / min(10, n)


