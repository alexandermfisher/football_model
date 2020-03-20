import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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

def E0_candidates():

    df = pd.read_csv('https://www.football-data.co.uk/mmz4281/1920/E0.csv')
    df = df[['Date','HomeTeam','AwayTeam','FTHG','FTAG']]
    teams_list = get_team_list('https://www.football-data.co.uk/mmz4281/1920/E0.csv')
    results = np.zeros([20,2])
    for i in range(20):
        results[i,:] = team_query_outcome(df,teams_list[i])

    print(list(compress(teams_list,results[:,0])))
    print(list(compress(teams_list,results[:,1])))

    return 


def E1_candidates():

    df = pd.read_csv('https://www.football-data.co.uk/mmz4281/1920/E1.csvz')
    df = df[['Date','HomeTeam','AwayTeam','FTHG','FTAG']]
    teams_list = get_team_list('https://www.football-data.co.uk/mmz4281/1920/E1.csv')
    results = np.zeros([20,2])
    for i in range(20):
        results[i,:] = team_query_outcome(df,teams_list[i])

    print(list(compress(teams_list,results[:,0])))
    print(list(compress(teams_list,results[:,1])))

    return 





E0_candidates()
E1_candidates()



















