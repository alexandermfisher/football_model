import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import csv
import football_model as fm
from itertools import compress
from datetime import date
import os

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

# download fixtures and upadate csv files with latest corrected fixtures stored in fixtures_files.
#fm.download_fixtures()


# finding valid bets. (missing 'League 1' 'League 2' 'Premier League' 'Bundesliga 2' 'Serie B' 'La Liga Segunda' 'Division 2')
# to add extra leagues add csv files into fixtures_files directory in the correct format and add to dictionary below with correct key and dic_value.
# e.g. key is league name (EPL) which is name of file, and dic_value is (E0) which corresponds to website.
leagues_dic = {'EPL': 'E0', 'Championship': 'E1','Bundesliga 1': 'D1', 'Serie A': 'I1','La Liga Primera':'SP1', 'Le Championnat': 'F1'}
fm.get_bets(leagues_dic)



#find weeks candidates and print to a txt file.
#fm.get_weekly_bets_txt(leagues_dictionary)

