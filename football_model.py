import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from itertools import compress

### Functions to compute win/loss ratio, and goal ratio. In addition taking the reusults and finding win and lose candidates

def team_query_outcome(dataframe,team):
    h_team_df = dataframe[dataframe['HomeTeam'] == team]
    h_team_df.reset_index(drop=True,inplace=True)
    h_team = h_team_df.to_numpy()
    h_team = h_team[-5:,3:5]

    a_team_df = dataframe[dataframe['AwayTeam'] == team]
    a_team_df.reset_index(drop=True,inplace=True)
    a_team = a_team_df.to_numpy()
    a_team = a_team[-5:,3:5]
    a_team = a_team[:,[1,0]]

    win_outcome = win_candidate(win_ratio(h_team),goal_ratio(h_team))
    lose_outcome = lose_candidate(win_ratio(a_team),goal_ratio(a_team))

    return win_outcome, lose_outcome

def win_ratio(team_data):
    win_count = 0
    for i in range(5):
        if team_data[i,0] > team_data[i,1]:
            win_count = win_count + 1
    win_ratio = win_count/5      
    return  win_ratio

def goal_ratio(team_data):

    sum_goals = np.sum(team_data, axis=0)

    return sum_goals[0]/sum_goals[1]

def win_candidate(win_ratio, goal_ratio):

    if win_ratio >= 0.7 and goal_ratio >= 2:
        return int(1)
    else:
        return int(0)

def lose_candidate(win_ratio,goal_ratio):

    if win_ratio <= 30 and goal_ratio <= 0.5:
        return int(1)
    else:
        return int(0)

def setdiff_sorted(array1,array2,assume_unique=False):
    ans = np.setdiff1d(array1,array2,assume_unique).tolist()
    if assume_unique:
        return sorted(ans)
    return ans

def get_team_list(url):
    df = pd.read_csv(url)
    df = df[['HomeTeam']]
    teams_list = setdiff_sorted(df.to_numpy(),[None])

    return teams_list

def league_candidates(league_id):

    df = pd.read_csv('https://www.football-data.co.uk/mmz4281/1920/' + league_id + '.csv')
    df = df[['Date','HomeTeam','AwayTeam','FTHG','FTAG']]
    teams_list = get_team_list('https://www.football-data.co.uk/mmz4281/1920/' + league_id + '.csv')
    results = np.zeros([int(len(teams_list)),2])
    for i in range(int(len(teams_list))):
        results[i,:] = team_query_outcome(df,teams_list[i])

    return list(compress(teams_list,results[:,0])), list(compress(teams_list,results[:,1]))

def get_weekly_bets():
    file = open("weekly_bets.txt","w+")
    for key in leagues_dictionary:
        win_candidates,lose_candidates = league_candidates(leagues_dictionary[key])  
        file.write(key+' win candidates:'+str(win_candidates)[1:-1]+ '\n')
        file.write(key+' lose candidates:'+str(lose_candidates)[1:-1]+ '\n\n')

    file.close()
    return  


list_leagues = ['EPL','Championship','League 1','League 2','Premier League','Bundesliga 1','Serie A','Serie B','La Liga Primera',
                'La Liga Segunda','Le Championnat',' Division 2']
leagues_dictionary = {'EPL': 'E0', 'Championship': 'E1', 'League 1': 'E2','League 2': 'E3','Premier League': 'SC0','Bundesliga 1': 'D1', 'Bundesliga 2': 'D2', 
                        'Serie A': 'I1','Serie B': 'I2','La Liga Primera':'SP1','La Liga Segunda':'SP2', 'Le Championnat': 'F1','Division 2':'F2'}

get_weekly_bets()










