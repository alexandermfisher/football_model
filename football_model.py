import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
from itertools import compress
import datetime as dt
from datetime import date
import urllib.request

#------------------------------------------------------------------------------------#
# CALCULATING WIN/LOSS RATIOS AND TEAM_OUTCOMES:
# exeucting thr kerel of the model. calculate for each team in the
# league whether they can be classed as a win or loss candidate

global win_points_ratio_var,win_goal_ratio_var,loss_points_ratio_var,loss_goal_ratio_var,games_played_var

games_played_var = 4
win_points_ratio_var = 0.8
win_goal_ratio_var = 2.5
loss_points_ratio_var = 0.2
loss_goal_ratio_var = 0.5



def win_points_ratio(team_data):

    win_points = 0
    for i in range(games_played_var):
        if team_data[i,0] > team_data[i,1]:
            win_points = win_points+3
        elif team_data[i,0] == team_data[i,1]:
            win_points = win_points + 1
        else:
            win_points = win_points

    return win_points/(3*games_played_var)

def goal_ratio(team_data):

    sum_goals = np.sum(team_data, axis=0)
    if sum_goals[1] == 0:
        ratio = 1.5
    else:
        ratio = (sum_goals[0])/(sum_goals[1])


    return ratio

def win_candidate(win_points_ratio, goal_ratio):

    if win_points_ratio >= win_points_ratio_var and goal_ratio >= win_goal_ratio_var:
        return int(1)
    else:
        return int(0)

def lose_candidate(win_points_ratio,goal_ratio):

    if win_points_ratio <= loss_points_ratio_var and goal_ratio <= loss_goal_ratio_var:
        return int(1)
    else:
        return int(0)

def team_query_outcome(dataframe,team):
    h_team_df = dataframe[dataframe['HomeTeam'] == team]
    h_team_df.reset_index(drop=True,inplace=True)
    h_team = h_team_df.to_numpy()
    h_team = h_team[-games_played_var:,3:5]

    a_team_df = dataframe[dataframe['AwayTeam'] == team]
    a_team_df.reset_index(drop=True,inplace=True)
    a_team = a_team_df.to_numpy()
    a_team = a_team[-games_played_var:,3:5]
    a_team = a_team[:,[1,0]]

    win_outcome = win_candidate(win_points_ratio(h_team),goal_ratio(h_team))
    lose_outcome = lose_candidate(win_points_ratio(a_team),goal_ratio(a_team))

    return win_outcome, lose_outcome

#-------------------------------------------------------------------------------------#
# GETTING TEAM LIST AND FIDING LEAGUE WIN/LOSS CANDIDATES AND VALID BETS:
# downloading results data and getting a list of teams and then executing 
# team_query_outcome to find league candiadates 
# downloading fixture list and comparing to candidates to output weekly_bets txt file.

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
    

    return [list(compress(teams_list,results[:,0])),list(compress(teams_list,results[:,1]))]

def get_weekly_bets_txt(leagues_dictionary):
    file = open("weekly_candidates.txt","w+")
    win_list = []
    lose_list = []
    for key in leagues_dictionary:
        win_candidates,lose_candidates = league_candidates(leagues_dictionary[key])
        for i in range(np.shape(win_candidates)[0]):    win_list.append(win_candidates[i])
        for i in range(np.shape(lose_candidates)[0]):   lose_list.append(lose_candidates[i])
        
        file.write(key+' win candidates:'+str(win_candidates)[1:-1]+ '\n')
        file.write(key+' lose candidates:'+str(lose_candidates)[1:-1]+ '\n\n')

    file.close()
    return

def download_fixtures_inner(urls_dic):
    for key in urls_dic:
        urllib.request.urlretrieve(urls_dic[key],'/Users/alexandermfisher/Documents/football_model_repositry/fixtures_files/'+key+'.csv')
    return

def download_fixtures():
    urls_dictionary = {'EPL':'https://fixturedownload.com/download/epl-2019-GMTStandardTime.csv',
    'Championship':'https://fixturedownload.com/download/championship-2019-GMTStandardTime.csv',
    'Bundesliga 1':'https://fixturedownload.com/download/bundesliga-2019-UTC.csv', 
    'Serie A': 'https://fixturedownload.com/download/serie-a-2019-WEuropeStandardTime.csv',
    'La Liga Primera': 'https://fixturedownload.com/download/la-liga-2019-RomanceStandardTime.csv',
    'Le Championnat':'https://fixturedownload.com/download/ligue-1-2019-RomanceStandardTime.csv'}
    download_fixtures_inner(urls_dictionary)
    return

def get_weeks_fixtures(league_key):
    df = pd.read_csv('/Users/alexandermfisher/Documents/football_model_repositry/fixtures_files/'+league_key+'.csv')
    df = df[['Date','Home Team','Away Team']]
    df['Date'] = pd.to_datetime(df['Date'],dayfirst=True)
    today = pd.Timestamp(date.today())
    plus_week = dt.timedelta(days = 7)
    #df.to_csv('output1.csv')
    df = df[(today <= df['Date']) & (df['Date'] <= today+plus_week)]
    df = df[['Home Team','Away Team']]
    fixtures = df.to_numpy()
    
    return fixtures

def get_bets(leagues_dictionary):
    file = open("weekly_bets.txt","w+")
    fixture_list = []
    for key in leagues_dictionary:
        candidates = league_candidates(leagues_dictionary[key])
        for i in range(len(get_weeks_fixtures(key)[:,0])):
            if get_weeks_fixtures(key)[i,0] in candidates[0]:
                    if get_weeks_fixtures(key)[i,1] in candidates[1]:
                        fixture_list.append([get_weeks_fixtures(key)[i,0],get_weeks_fixtures(key)[i,1]])
                        file.write(key+': '+get_weeks_fixtures(key)[i,0]+' vs '+get_weeks_fixtures(key)[i,1]+'\n')
                   
    file.close()
    return







