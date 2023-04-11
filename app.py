import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
import numpy as np
import math
from scipy import stats
from PIL import Image
from mplsoccer import PyPizza, add_image, FontManager
from matplotlib import font_manager
from matplotlib.patches import Circle, Rectangle, Arc

import matplotlib as mpl
mpl.rcParams["axes.spines.right"] = True
mpl.rcParams["axes.spines.top"] = True
mpl.rcParams["axes.spines.left"] = True
mpl.rcParams["axes.spines.bottom"] = True

st.set_page_config(layout="wide")

st.set_option('deprecation.showPyplotGlobalUse', False)

# DATA
@st.experimental_memo
def load_data(url):
    df = pd.read_csv(url)
    return df

def load_shot_data(url):
    df_shots = pd.read_csv(url)
    return df_shots

df = load_data("Data.csv")
df_shots = load_shot_data("Shot_Data.csv")

font_dirs = ["//Users//sissigarduno//Downloads"]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

plt.rcParams['font.family'] = "Poppins"
plt.rcParams['font.size'] = '10.6'

image = Image.open("Logos/BetclicElite.png")
st.sidebar.image(image)

# FILTERS
st.sidebar.header('Filters')
st.sidebar.write("Select a range of rounds :")
begin = st.sidebar.slider('First game :', 1, 34, 1)
end = st.sidebar.slider('Last game :', 1, 34, 34)
location = st.sidebar.selectbox('Home / Away :', ('All', 'Home', 'Away'))

# FILETRING DATA
df1 = df[df['round'].between(begin, end)]
df1['Pace'] = df1["2FGA"] + df1["3FGA"] + 0.44*df1["FTA"] - df1["OREB"] + df1["TOV"]

# DATA TREATMENT
# Home
hometeam = df1.groupby(['home_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
hometeam = hometeam.drop(hometeam[hometeam.home_team != hometeam.team_id].index)
hometeam = hometeam.drop('team_id', axis=1)
hometeam.rename(columns={'home_team': 'Team_name'}, inplace=True)

homeopp = df1.groupby(['home_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
homeopp = homeopp.drop(homeopp[homeopp.home_team == homeopp.team_id].index)
homeopp = homeopp.groupby(['home_team']).agg({'Nb_games': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'PTS':'PTS opp', 'Pace':'Pace opp',
                                                    '2FGM':'2FGM opp', '2FGA':'2FGA opp', '3FGM':'3FGM opp', '3FGA':'3FGA opp', 'FTM':'FTM opp', 'FTA':'FTA opp',
                                                    'OREB':'OREB opp', 'DREB':'DREB opp', 'AST':'AST opp', 'STL':'STL opp', 'TOV':'TOV opp', 'BLK':'BLK opp',
                                                    'BLKA':'BLKA opp', 'PF':'PF opp'})
homeopp.rename(columns={'home_team': 'Team_name'}, inplace=True)

# Away
awayteam = df1.groupby(['away_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
awayteam = awayteam.drop(awayteam[awayteam.away_team != awayteam.team_id].index)
awayteam = awayteam.drop('team_id', axis=1)
awayteam.rename(columns={'away_team': 'Team_name'}, inplace=True)

awayopp = df1.groupby(['away_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
awayopp = awayopp.drop(awayopp[awayopp.away_team == awayopp.team_id].index)
awayopp = awayopp.groupby(['away_team']).agg({'Nb_games': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'PTS':'PTS opp', 'Pace':'Pace opp',
                                                    '2FGM':'2FGM opp', '2FGA':'2FGA opp', '3FGM':'3FGM opp', '3FGA':'3FGA opp', 'FTM':'FTM opp', 'FTA':'FTA opp',
                                                    'OREB':'OREB opp', 'DREB':'DREB opp', 'AST':'AST opp', 'STL':'STL opp', 'TOV':'TOV opp', 'BLK':'BLK opp',
                                                    'BLKA':'BLKA opp', 'PF':'PF opp'})
awayopp.rename(columns={'away_team': 'Team_name'}, inplace=True)

if location == "Home":
    resultteam = hometeam
    resultopp = homeopp
elif location == "Away":
    resultteam = awayteam
    resultopp = awayopp
else:
    resultteam = pd.concat([hometeam, awayteam])
    resultopp = pd.concat([homeopp, awayopp])
    
resultteam = resultteam.groupby(['Team_name']).agg({'Nb_games':'sum', 'PTS':'sum','Pace':'sum','2FGM':'sum','2FGA':'sum', '3FGM':'sum','3FGA':'sum','FTM':'sum',
                                             'FTA':'sum','OREB':'sum','DREB':'sum', 'AST':'sum','STL':'sum', 'TOV':'sum','BLK':'sum','BLKA':'sum', 'PF':'sum'})
resultopp = resultopp.groupby(['Team_name']).agg({'PTS opp':'sum','Pace opp':'sum','2FGM opp':'sum','2FGA opp':'sum', '3FGM opp':'sum','3FGA opp':'sum'
                                                  ,'FTM opp':'sum', 'FTA opp':'sum','OREB opp':'sum','DREB opp':'sum', 'AST opp':'sum','STL opp':'sum', 'TOV opp':'sum'
                                                  ,'BLK opp':'sum','BLKA opp':'sum', 'PF opp':'sum'})

result = pd.concat([resultteam, resultopp])
result = result.groupby(['Team_name']).agg({'Nb_games':'sum', 'PTS':'sum','Pace':'sum','2FGM':'sum','2FGA':'sum', '3FGM':'sum','3FGA':'sum','FTM':'sum',
                                             'FTA':'sum','OREB':'sum','DREB':'sum', 'AST':'sum','STL':'sum', 'TOV':'sum','BLK':'sum','BLKA':'sum', 'PF':'sum', 
                                             'PTS opp':'sum','Pace opp':'sum','2FGM opp':'sum','2FGA opp':'sum', '3FGM opp':'sum','3FGA opp':'sum','FTM opp':'sum',
                                             'FTA opp':'sum','OREB opp':'sum','DREB opp':'sum', 'AST opp':'sum','STL opp':'sum', 'TOV opp':'sum', 'BLK opp':'sum',
                                             'BLKA opp':'sum', 'PF opp':'sum'})
result = result.rename_axis('Team_name').reset_index()

# DATA CALCULATION
result['ORTG'] = result['PTS'] / result['Pace'] * 100
result['DRTG'] = result['PTS opp'] / result['Pace opp'] * 100
result['NetRTG'] = result['ORTG'] - result['DRTG']
result['eFG%'] = ((result['2FGM'] + result['3FGM']*1.5) / (result['2FGA'] + result['3FGA'])) * 100
result['eFG% opp'] = ((result['2FGM opp'] + result['3FGM opp']*1.5) / (result['2FGA opp'] + result['3FGA opp'])) * 100
result['TS%'] = (result['PTS'] / (2*((result['2FGA'] + result['3FGA']) + 0.44*result['FTA']))) * 100
result['TS% opp'] = (result['PTS opp'] / (2*((result['2FGA opp'] + result['3FGA opp']) + 0.44*result['FTA opp']))) * 100
result['AST/TO'] = result['AST'] / result['TOV']
result['AST/TO opp'] = result['AST opp'] / result['TOV opp']
result['TOV%'] = (result['TOV'] / result['Pace']) * 100
result['TOV% opp'] = (result['TOV opp'] / result['Pace opp']) * 100
result['OREB%'] = (result['OREB'] / (result['OREB'] + result['DREB opp'])) * 100
result['OREB% opp'] = (result['OREB opp'] / (result['OREB opp'] + result['DREB'])) * 100
result['DREB%'] = (result['DREB'] / (result['DREB'] + result['OREB opp'])) * 100
result['DREB% opp'] = (result['DREB opp'] / (result['DREB opp'] + result['OREB'])) * 100
result['BLK%'] = (result['BLK'] / (result['2FGA opp'] + result['3FGA opp'])) * 100
result['BLK% opp'] = (result['BLK opp'] / (result['2FGA'] + result['3FGA'])) * 100
result['STL%'] = (result['STL'] / result['Pace opp']) * 100
result['STL% opp'] = (result['STL opp'] / result['Pace']) * 100
result['Poss/G'] = result['Pace'] / result['Nb_games']
result['Poss/G opp'] = result['Pace opp'] / result['Nb_games']
result['FTAr'] = (result['FTA'] / (result['2FGA'] + result['3FGA'])) * 100
result['FTAr opp'] = (result['FTA opp'] / (result['2FGA opp'] + result['3FGA opp'])) * 100
result['2P%'] = (result['2FGM'] / result['2FGA'])*100
result['2P% opp'] = (result['2FGM opp'] / result['2FGA opp'])*100
result['3P%'] = (result['3FGM'] / result['3FGA'])*100
result['3P% opp'] = (result['3FGM opp'] / result['3FGA opp'])*100
result['FT%'] = (result['FTM'] / result['FTA'])*100
result['FT% opp'] = (result['FTM opp'] / result['FTA opp'])*100
result["FGA% 2PT"] = (result["2FGA"] / (result["2FGA"] + result["3FGA"])) * 100
result["FGA% 3PT"] = (result["3FGA"] / (result["2FGA"] + result["3FGA"])) * 100
result["PTS% 2PT"] = (result["2FGM"]*2 / (result["2FGM"]*2 + result["3FGM"]*3 + result["FTM"])) * 100
result["PTS% 3PT"] = (result["3FGM"]*3 / (result["2FGM"]*2 + result["3FGM"]*3 + result["FTM"])) * 100
result["PTS% FT"] = (result["FTM"] / (result["2FGM"]*2 + result["3FGM"]*3 + result["FTM"])) * 100
result["FGM% AST"] = (result["AST"] / (result["2FGM"] + result["3FGM"])) * 100
result["FGM% UAST"] = (1-(result["AST"] / (result["2FGM"] + result["3FGM"]))) * 100
result["FGA% 2PT opp"] = (result["2FGA opp"] / (result["2FGA opp"] + result["3FGA opp"])) * 100
result["FGA% 3PT opp"] = (result["3FGA opp"] / (result["2FGA opp"] + result["3FGA opp"])) * 100
result["PTS% 2PT opp"] = (result["2FGM opp"]*2 / (result["2FGM opp"]*2 + result["3FGM opp"]*3 + result["FTM opp"])) * 100
result["PTS% 3PT opp"] = (result["3FGM opp"]*3 / (result["2FGM opp"]*2 + result["3FGM opp"]*3 + result["FTM opp"])) * 100
result["PTS% FT opp"] = (result["FTM opp"] / (result["2FGM opp"]*2 + result["3FGM opp"]*3 + result["FTM opp"])) * 100
result["FGM% AST opp"] = (result["AST opp"] / (result["2FGM opp"] + result["3FGM opp"])) * 100
result["FGM% UAST opp"] = (1-(result["AST opp"] / (result["2FGM opp"] + result["3FGM opp"]))) * 100
result['PTS/G'] = result['PTS'] / result['Nb_games']
result['2PM/G'] = result['2FGM'] / result['Nb_games']
result['2PA/G'] = result['2FGA'] / result['Nb_games']
result['3PM/G'] = result['3FGM'] / result['Nb_games']
result['3PA/G'] = result['3FGA'] / result['Nb_games']
result['FTM/G'] = result['FTM'] / result['Nb_games']
result['FTA/G'] = result['FTA'] / result['Nb_games']
result['OREB/G'] = result['OREB'] / result['Nb_games']
result['DREB/G'] = result['DREB'] / result['Nb_games']
result['TREB/G'] = (result['OREB'] + result['DREB']) / result['Nb_games']
result['AST/G'] = result['AST'] / result['Nb_games']
result['STL/G'] = result['STL'] / result['Nb_games']
result['TOV/G'] = result['TOV'] / result['Nb_games']
result['BLK/G'] = result['BLK'] / result['Nb_games']
result['BLKA/G'] = result['BLKA'] / result['Nb_games']
result['PF/G'] = result['PF'] / result['Nb_games']
result['PTS/G opp'] = result['PTS opp'] / result['Nb_games']
result['2PM/G opp'] = result['2FGM opp'] / result['Nb_games']
result['2PA/G opp'] = result['2FGA opp'] / result['Nb_games']
result['3PM/G opp'] = result['3FGM opp'] / result['Nb_games']
result['3PA/G opp'] = result['3FGA opp'] / result['Nb_games']
result['FTM/G opp'] = result['FTM opp'] / result['Nb_games']
result['FTA/G opp'] = result['FTA opp'] / result['Nb_games']
result['OREB/G opp'] = result['OREB opp'] / result['Nb_games']
result['DREB/G opp'] = result['DREB opp'] / result['Nb_games']
result['TREB/G opp'] = (result['OREB opp'] + result['DREB opp']) / result['Nb_games']
result['AST/G opp'] = result['AST opp'] / result['Nb_games']
result['STL/G opp'] = result['STL opp'] / result['Nb_games']
result['TOV/G opp'] = result['TOV opp'] / result['Nb_games']
result['BLK/G opp'] = result['BLK opp'] / result['Nb_games']
result['BLKA/G opp'] = result['BLKA opp'] / result['Nb_games']
result['PF/G opp'] = result['PF opp'] / result['Nb_games']

# TEAM FILTER
st.sidebar.write("Select a team : ")
teamname = hometeam['Team_name']
teamselection = st.sidebar.selectbox('Team :',("Paris", "Blois", "Boulogne-Levallois", "Bourg-en-Bresse", "Cholet", "Dijon", "Fos-sur-Mer", "Gravelines-Dunkerque",
                                               "Le Mans", "Le Portel", "Limoges", "Lyon-Villeurbanne", "Monaco", "Nancy", "Nanterre", "Pau-Lacq-Orthez",
                                               "Roanne", "Strasbourg"), label_visibility="collapsed")
st.sidebar.write("##")
st.sidebar.write('*Rounds available : from ',df['round'].min(),' to ', df['round'].max())

#VIZ 1
#Graph
result.sort_index()
def getImage(path, zoom=1):
    return OffsetImage(plt.imread(path), zoom=0.225)

paths = [
    'Logos/Blois.png',
    'Logos/Boulogne-Levallois.png',
    'Logos/Bourg-en-Bresse.png',
    'Logos/Cholet.png',
    'Logos/Dijon.png',
    'Logos/Fos-sur-Mer.png',
    'Logos/Gravelines-Dunkerque.png',
    'Logos/Le Mans.png',
    'Logos/Le Portel.png',
    'Logos/Limoges.png',
    'Logos/Lyon-Villeurbanne.png',
    'Logos/Monaco.png',
    'Logos/Nancy.png',
    'Logos/Nanterre.png',
    'Logos/Paris.png',
    'Logos/Pau-Lacq-Orthez.png',
    'Logos/Roanne.png',
    'Logos/Strasbourg.png'
]
    
x = result['ORTG']
y = result['DRTG']

fig, ax = plt.subplots()
ax.scatter(x, y, c="white") 
# Move left y-axis and bottom x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('center')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# Others
ax.invert_yaxis()
ax.tick_params(axis='both', which='major', labelsize=8)
#ax.text(96, 92, 'Net +5', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.text(100.8, 92, 'Net +10', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.text(105.8, 92, 'Net +15', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.text(90, 95.8, 'Net -5', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.text(90, 101, 'Net -10', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.text(91, 107, 'Net -15', rotation = -35, fontsize = 'xx-small', c="lightgrey")
#ax.plot([85, 125], [90, 130], ls="--", c="lightgrey", linewidth=0.5)
#ax.plot([85, 120], [95, 130], ls="--", c="lightgrey", linewidth=0.5)
#ax.plot([85, 115], [100, 130], ls="--", c="lightgrey", linewidth=0.5)
#ax.plot([90, 130], [85, 125], ls="--", c="lightgrey", linewidth=0.5)
#ax.plot([95, 130], [85, 120], ls="--", c="lightgrey", linewidth=0.5)
#ax.plot([100, 130], [85, 115], ls="--", c="lightgrey", linewidth=0.5)
maxORTG = result['ORTG'].max()+1
minORTG = result['ORTG'].min()-1
maxDRTG = result['DRTG'].max()+1
minDRTG = result['DRTG'].min()-1
avgORTG = (maxORTG + minORTG)/2
avgDRTG = (maxDRTG + minDRTG)/2
DRTGx= avgORTG + 0.2
DRTGy= maxDRTG
ORTGx= minORTG
ORTGy= avgDRTG - 0.2
ax.text(DRTGx, DRTGy, 'Defensive Rating', rotation = 'vertical', fontsize = 'xx-small')
ax.text(ORTGx, ORTGy, 'Offensive Rating', rotation = 'horizontal', fontsize = 'xx-small')
ax.plot([minORTG, maxORTG], [minDRTG, maxDRTG], ls="--", c="lightgrey", linewidth=1)
x1 = minORTG + 0.5
y1 = minDRTG + 2
ax.text(x1, y1, 'Positive Teams', rotation = -35, fontsize = 'xx-small', c="lightgrey", weight='bold')
x2 = minORTG
y2 = minDRTG + 3
ax.text(x2, y2, 'Negative Teams', rotation = -35, fontsize = 'xx-small', c="lightgrey", weight='bold')
ax.set(xlim=(minORTG, maxORTG), ylim=(maxDRTG, minDRTG))

for x0, y0, path in zip(x, y,paths):
    ab = AnnotationBbox(getImage(path), (x0, y0), frameon=False)
    ax.add_artist(ab)
    
# VIZ 2
params = ['ORTG', 'eFG%', 'TS%', 'AST/TO', 'TOV%', 'OREB%', 'DRTG', 'DREB%', 'BLK%', 'STL%', 'NetRTG', 'Poss/G', 'FTAr']

pizza = (result[['Team_name', 'ORTG', 'eFG%', 'TS%', 'AST/TO', 'TOV%', 'OREB%', 'DRTG', 'DREB%', 'BLK%', 'STL%', 'NetRTG', 'Poss/G', 'FTAr']])
pizza = pizza.fillna(0)

team = pizza.loc[pizza['Team_name'] == teamselection].reset_index()
team = list(team.loc[0])
team = team[2:]

values = []
for x in range(len(params)):
    values.append(math.floor(stats.percentileofscore(pizza[params[x]], team[x])))
    
values[4] = 100 - values[4]
values[6] = 100 - values[6]

    
 # color for the slices and text
slice_colors = ["#1A78CF"] * 3 + ["#FF9300"] * 3 + ["#D70232"] * 4 + ["grey"] * 3
box_colors = ["white"] * 13
box_font_colors = ["#252528"] * 13
text_colors = ["black"] * 13

# instantiate PyPizza class
baker = PyPizza(
    params=params,  # list of parameters
    background_color="#FFFFFF",  # background color
    straight_line_color="white",  # color for straight lines
    straight_line_lw=1,  # linewidth for straight lines
    last_circle_lw=0,  # linewidth of last circle
    other_circle_lw=0,  # linewidth for other circles
    inner_circle_size=0  # size of inner circle
)

# plot pizza
fig1, ax = baker.make_pizza(
    values,  # list of values
    figsize=(8, 8.5),  # adjust figsize according to your need
    color_blank_space="same",  # use same color to fill blank space
    slice_colors=slice_colors,  # color for individual slices
    value_colors=box_colors,  # color for the value-text
    value_bck_colors=box_font_colors,  # color for the blank spaces
    blank_alpha=0.4,# alpha for blank-space colors
    kwargs_slices=dict(
        edgecolor="#212124", zorder=2, linewidth=1
    ),  # values to be used when plotting slices
    kwargs_params=dict(
        color="black", fontsize=11,
        va="center"
    ),  # values to be used when adding parameter
    kwargs_values=dict(
        color="black", fontsize=11,
        zorder=3,
        bbox=dict(
            edgecolor="black", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )  # values to be used when adding parameter-values
)

#Legend
# add text
fig1.text(0.5, 0.97, teamselection, size=20, color="#000000", ha="center")
fig1.text(
    0.1, 0.925, "Attacking", size=10, color="#000000"
)
fig1.text(
    0.1, 0.900, "Possession", size=10, color="#000000"
)
fig1.text(
    0.1, 0.875, "Defending", size=10, color="#000000"
)
fig1.text(
    0.1, 0.850, "Other", size=10, color="#000000"
)

# add rectangles
fig1.patches.extend([
    plt.Rectangle(
        (0.06, 0.922), 0.025, 0.021, fill=True, color="#1a78cf",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.897), 0.025, 0.021, fill=True, color="#ff9300",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.872), 0.025, 0.021, fill=True, color="#d70232",
        transform=fig1.transFigure, figure=fig1
    ),
    plt.Rectangle(
        (0.06, 0.847), 0.025, 0.021, fill=True, color="grey",
        transform=fig1.transFigure, figure=fig1
    ),
])
# SHOOTING VIZ
df_shots = df_shots[df_shots['round'].between(begin, end)]
home_df = df_shots[df_shots['team_id'] == teamselection]
home_df['distance'] = np.sqrt(home_df['x']**2 + home_df['y']**2)

def f(row):
    if row['distance'] > 6.75:
        val = "3pts"
    elif row['distance'] > 4.5:
        val = "Long 2"
    elif row['distance'] > 2.5:
        val = "Short 2"
    elif row['distance'] > 1.2:
        val = "Paint"
    elif row['distance'] > 0:
        val = "Rim"
    else:
        val = "ERROR"
    return val

home_df['zone_details'] = home_df.apply(f, axis=1)

# Bar Chart for shooting
params1 = ['Rim', 'Paint', 'Short 2', 'Long 2', '3pts']
params2 = ['Rim', 'Paint', 'Short 2', 'Long 2', '3pts']

#Team
def test(df, value_to_check):
    df = df.set_index('id')
    dtypes = df.dtypes
    df.loc[value_to_check, ['value']] = 0
    return df.astype(dtypes).reset_index()

shootingdf = home_df.groupby(['type', 'zone_details']).agg({'action_number': 'count'}).reset_index()
rim = shootingdf[shootingdf['zone_details'] == 'Rim']
rim = rim.set_index('type')
rim = rim.T
rim = rim.drop(labels="zone_details")
rim = test(rim, "2FGM")
teamrim = rim['2FGM'] / (rim['2FGM'] + rim['2FGA']) * 100
paint = shootingdf[shootingdf['zone_details'] == 'Paint']
paint = paint.set_index('type')
paint = paint.T
paint = paint.drop(labels="zone_details")
paint = test(paint, "2FGM")
teampaint = paint['2FGM'] / (paint['2FGM'] + paint['2FGA']) * 100
short2 = shootingdf[shootingdf['zone_details'] == 'Short 2']
short2 = short2.set_index('type')
short2 = short2.T
short2 = short2.drop(labels="zone_details")
short2 = test(short2, "2FGM")
teamshort2 = short2['2FGM'] / (short2['2FGM'] + short2['2FGA']) * 100
long2 = shootingdf[shootingdf['zone_details'] == 'Long 2']
long2 = long2.set_index('type')
long2 = long2.T
long2 = long2.drop(labels="zone_details")
long2 = test(long2, "2FGM")
teamlong2 = long2['2FGM'] / (long2['2FGM'] + long2['2FGA']) * 100
three = shootingdf[shootingdf['zone_details'] == '3pts']
three = three.set_index('type')
three = three.T
three = three.drop(labels="zone_details")
three = test(three, "3FGM")
teamthree = three['3FGM'] / (three['3FGM'] + three['3FGA']) * 100
bar1 = pd.concat([teamrim, teampaint, teamshort2, teamlong2, teamthree], axis=1)
bar1 = bar1.T
team1 = bar1["action_number"].tolist()

shootingdf = home_df.groupby(['type', 'zone_details']).agg({'action_number': 'count'}).reset_index()
rim = shootingdf[shootingdf['zone_details'] == 'Rim']
rim = rim.set_index('type')
rim = rim.T
rim = rim.drop(labels="zone_details")
rim = test(rim, "2FGM")
teamrim = (rim['2FGM'] + rim['2FGA'])
paint = shootingdf[shootingdf['zone_details'] == 'Paint']
paint = paint.set_index('type')
paint = paint.T
paint = paint.drop(labels="zone_details")
paint = test(paint, "2FGM")
teampaint = (paint['2FGM'] + paint['2FGA'])
short2 = shootingdf[shootingdf['zone_details'] == 'Short 2']
short2 = short2.set_index('type')
short2 = short2.T
short2 = short2.drop(labels="zone_details")
short2 = test(short2, "2FGM")
teamshort2 = (short2['2FGM'] + short2['2FGA'])
long2 = shootingdf[shootingdf['zone_details'] == 'Long 2']
long2 = long2.set_index('type')
long2 = long2.T
long2 = long2.drop(labels="zone_details")
long2 = test(long2, "2FGM")
teamlong2 = (long2['2FGM'] + long2['2FGA'])
three = shootingdf[shootingdf['zone_details'] == '3pts']
three = three.set_index('type')
three = three.T
three = three.drop(labels="zone_details")
three = test(three, "3FGM")
teamthree = (three['3FGM'] + three['3FGA'])
bar2 = pd.concat([teamrim, teampaint, teamshort2, teamlong2, teamthree], axis=1)
bar2['tot'] = bar2[0] + bar2[1] + bar2[2] + bar2[3] + bar2[4]
bar2[0] = bar2[0] / bar2['tot'] * 100
bar2[1] = bar2[1] / bar2['tot'] * 100
bar2[2] = bar2[2] / bar2['tot'] * 100
bar2[3] = bar2[3] / bar2['tot'] * 100
bar2[4] = bar2[4] / bar2['tot'] * 100
bar2 = bar2.drop(columns=['tot'])
bar2 = bar2.T
team2 = bar2["action_number"].tolist()

#League
df_shots['distance'] = np.sqrt(df_shots['x']**2 + df_shots['y']**2)

def f(row):
    if row['distance'] > 6.75:
        val = "3pts"
    elif row['distance'] > 4.5:
        val = "Long 2"
    elif row['distance'] > 2.5:
        val = "Short 2"
    elif row['distance'] > 1.2:
        val = "Paint"
    elif row['distance'] > 0:
        val = "Rim"
    else:
        val = "ERROR"
    return val

df_shots['zone_details'] = df_shots.apply(f, axis=1)

shootingdf = df_shots.groupby(['type', 'zone_details']).agg({'action_number': 'count'}).reset_index()
rim = shootingdf[shootingdf['zone_details'] == 'Rim']
rim = rim.set_index('type')
rim = rim.T
rim = rim.drop(labels="zone_details")
leaguerim = rim['2FGM'] / (rim['2FGM'] + rim['2FGA']) * 100
paint = shootingdf[shootingdf['zone_details'] == 'Paint']
paint = paint.set_index('type')
paint = paint.T
paint = paint.drop(labels="zone_details")
leaguepaint = paint['2FGM'] / (paint['2FGM'] + paint['2FGA']) * 100
short2 = shootingdf[shootingdf['zone_details'] == 'Short 2']
short2 = short2.set_index('type')
short2 = short2.T
short2 = short2.drop(labels="zone_details")
leagueshort2 = short2['2FGM'] / (short2['2FGM'] + short2['2FGA']) * 100
long2 = shootingdf[shootingdf['zone_details'] == 'Long 2']
long2 = long2.set_index('type')
long2 = long2.T
long2 = long2.drop(labels="zone_details")
leaguelong2 = long2['2FGM'] / (long2['2FGM'] + long2['2FGA']) * 100
three = shootingdf[shootingdf['zone_details'] == '3pts']
three = three.set_index('type')
three = three.T
three = three.drop(labels="zone_details")
leaguethree = three['3FGM'] / (three['3FGM'] + three['3FGA']) * 100
league1 = pd.concat([leaguerim, leaguepaint, leagueshort2, leaguelong2, leaguethree], axis=1)
league1 = league1.T
league1 = league1["action_number"].tolist()

rim = shootingdf[shootingdf['zone_details'] == 'Rim']
rim = rim.set_index('type')
rim = rim.T
rim = rim.drop(labels="zone_details")
leaguerim = (rim['2FGM'] + rim['2FGA'])
paint = shootingdf[shootingdf['zone_details'] == 'Paint']
paint = paint.set_index('type')
paint = paint.T
paint = paint.drop(labels="zone_details")
leaguepaint = (paint['2FGM'] + paint['2FGA'])
short2 = shootingdf[shootingdf['zone_details'] == 'Short 2']
short2 = short2.set_index('type')
short2 = short2.T
short2 = short2.drop(labels="zone_details")
leagueshort2 = (short2['2FGM'] + short2['2FGA'])
long2 = shootingdf[shootingdf['zone_details'] == 'Long 2']
long2 = long2.set_index('type')
long2 = long2.T
long2 = long2.drop(labels="zone_details")
leaguelong2 = (long2['2FGM'] + long2['2FGA'])
three = shootingdf[shootingdf['zone_details'] == '3pts']
three = three.set_index('type')
three = three.T
three = three.drop(labels="zone_details")
leaguethree = (three['3FGM'] + three['3FGA'])
league2 = pd.concat([leaguerim, leaguepaint, leagueshort2, leaguelong2, leaguethree], axis=1)
league2['tot'] = league2[0] + league2[1] + league2[2] + league2[3] + league2[4]
league2[0] = league2[0] / league2['tot'] * 100
league2[1] = league2[1] / league2['tot'] * 100
league2[2] = league2[2] / league2['tot'] * 100
league2[3] = league2[3] / league2['tot'] * 100
league2[4] = league2[4] / league2['tot'] * 100
league2 = league2.drop(columns=['tot'])
league2 = league2.T
league2 = league2["action_number"].tolist()

teamrim = team1[0] + 8
teampaint = team1[1] + 8
teamshort2 = team1[2] + 8
teamlong2 = team1[3] + 8
teamthree = team1[4] + 8
teamfgarim = team2[0] + 8
teamfgapaint = team2[1] + 8
teamfgashort2 = team2[2] + 8
teamfgalong2 = team2[3] + 8
teamfgathree = team2[4] + 8
rim = league1[0]
paint = league1[1]
short2 = league1[2]
long2 = league1[3]
three = league1[4]
fgarim = league2[0]
fgapaint = league2[1]
fgashort2 = league2[2]
fgalong2 = league2[3]
fgathree = league2[4]
title = max(team2) + 10

fig3, axis = plt.subplots(2,1)
bar_container1 = axis[0].bar(params1, team1, width=0.5)
axis[0].set_title("Shooting % By Shot Type")
axis[0].spines['right'].set_visible(False)
axis[0].spines['left'].set_visible(False)
axis[0].spines['top'].set_visible(False)
axis[0].tick_params(axis='x', which='major', labelsize=8)
axis[0].set_yticklabels([])
axis[0].tick_params(left = False)
axis[0].tick_params(bottom = False)
axis[0].axhline(77, .447, .553, color='grey')
axis[0].text(2, 80, "League Avg.", color='black', fontsize=5, ha='center', va='center')
# Rim
axis[0].axhline(rim, .043, .15, color='grey')
axis[0].text(-0.4, rim, "{:.1f}%".format(rim), color='black', fontsize=5, ha='center', va='center')
axis[0].text(0, teamrim, "{:.1f}%".format(teamrim - 8), color='black', fontsize=10, ha='center', va='center')
# Paint
axis[0].axhline(paint, .244, .351, color='grey')
axis[0].text(0.6, paint, "{:.1f}%".format(paint), color='black', fontsize=5, ha='center', va='center')
axis[0].text(1, teampaint, "{:.1f}%".format(teampaint - 8), color='black', fontsize=10, ha='center', va='center')
# Short 2
axis[0].axhline(short2, .447, .554, color='grey')
axis[0].text(1.6, short2, "{:.1f}%".format(short2), color='black', fontsize=5, ha='center', va='center')
axis[0].text(2, teamshort2, "{:.1f}%".format(teamshort2 - 8), color='black', fontsize=10, ha='center', va='center')
# Long 2
axis[0].axhline(long2, .648, .755, color='grey')
axis[0].text(2.6, long2, "{:.1f}%".format(long2), color='black', fontsize=5, ha='center', va='center')
axis[0].text(3, teamlong2, "{:.1f}%".format(teamlong2 - 8), color='black', fontsize=10, ha='center', va='center')
# Three
axis[0].axhline(three, .85, .958, color='grey')
axis[0].text(3.6, three, "{:.1f}%".format(three), color='black', fontsize=5, ha='center', va='center')
axis[0].text(4, teamthree, "{:.1f}%".format(teamthree - 8), color='black', fontsize=10, ha='center', va='center')

bar_container2 = axis[1].bar(params2, team2, width=0.5)
axis[1].text(2, title-2, "Shot Selection Distribution", ha='center', va='center', fontsize=13)
axis[1].spines['right'].set_visible(False)
axis[1].spines['left'].set_visible(False)
axis[1].spines['top'].set_visible(False)
axis[1].tick_params(axis='x', which='major', labelsize=8)
axis[1].set_yticklabels([])
axis[1].tick_params(left = False)
axis[1].tick_params(bottom = False)
axis[1].set_ylim([0, title])
# FGA% Rim
axis[1].axhline(fgarim, .043, .15, color='grey')
axis[1].text(-0.4, fgarim, "{:.1f}%".format(fgarim), color='black', fontsize=5, ha='center', va='center')
axis[1].text(0, teamfgarim, "{:.1f}%".format(teamfgarim - 8), color='black', fontsize=10, ha='center', va='center')
# FGA% Paint
axis[1].axhline(fgapaint, .244, .351, color='grey')
axis[1].text(0.6, fgapaint, "{:.1f}%".format(fgapaint), color='black', fontsize=5, ha='center', va='center')
axis[1].text(1, teamfgapaint, "{:.1f}%".format(teamfgapaint - 8), color='black', fontsize=10, ha='center', va='center')
#FGA% Short 2
axis[1].axhline(fgashort2, .447, .554, color='grey')
axis[1].text(1.6, fgashort2, "{:.1f}%".format(fgashort2), color='black', fontsize=5, ha='center', va='center')
axis[1].text(2, teamfgashort2, "{:.1f}%".format(teamfgashort2 - 8), color='black', fontsize=10, ha='center', va='center')
# FGA% Long 2
axis[1].axhline(fgalong2, .648, .755, color='grey')
axis[1].text(2.6, fgalong2, "{:.1f}%".format(fgalong2), color='black', fontsize=5, ha='center', va='center')
axis[1].text(3, teamfgalong2, "{:.1f}%".format(teamfgalong2 - 8), color='black', fontsize=10, ha='center', va='center')
# FGA% Three
axis[1].axhline(fgathree, .85, .958, color='grey')
axis[1].text(3.6, fgathree, "{:.1f}%".format(fgathree), color='black', fontsize=5, ha='center', va='center')
axis[1].text(4, teamfgathree, "{:.1f}%".format(teamfgathree - 8), color='black', fontsize=10, ha='center', va='center')

# VIZ 4
def draw_court(ax=None, color='black', lw=1, outer_lines=True):
    """
    FIBA basketball court dimensions:
    https://www.msfsports.com.au/basketball-court-dimensions/
    It seems like the Euroleauge API returns the shooting positions
    in resolution of 1cm x 1cm.
    """
    # If an axes object isn't provided to plot onto, just get current one
    if ax is None:
        ax = plt.gca()

    # Create the various parts of an NBA basketball court

    # Create the basketball hoop
    # Diameter of a hoop is 45.72cm so it has a radius 45.72/2 cms
    hoop = Circle((0, 0), radius=45.72 / 2, linewidth=lw, color=color,
                  fill=False)

    # Create backboard
    backboard = Rectangle((-90, -157.5 + 120), 180, -1, linewidth=lw,
                          color=color)

    # The paint
    # Create the outer box of the paint
    outer_box = Rectangle((-490 / 2, -157.5), 490, 580, linewidth=lw,
                          color=color, fill=False)
    # Create the inner box of the paint, widt=12ft, height=19ft
    inner_box = Rectangle((-360 / 2, -157.5), 360, 580, linewidth=lw,
                          color=color, fill=False)

    # Create free throw top arc
    top_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=0, theta2=180,
                         linewidth=lw, color=color, fill=False)
    # Create free throw bottom arc
    bottom_free_throw = Arc((0, 580 - 157.5), 360, 360, theta1=180, theta2=0,
                            linewidth=lw, color=color, linestyle='dashed')
    # Restricted Zone, it is an arc with 4ft radius from center of the hoop
    restricted = Arc((0, 0), 2 * 125, 2 * 125, theta1=0, theta2=180,
                     linewidth=lw, color=color)

    # Three point line
    # Create the side 3pt lines
    corner_three_a = Rectangle((-750 + 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    corner_three_b = Rectangle((750 - 90, -157.5), 0, 305, linewidth=lw,
                               color=color)
    # 3pt arc - center of arc will be the hoop, arc is 23'9" away from hoop
    # I just played around with the theta values until they lined up with the
    # threes
    three_arc = Arc((0, 0), 2 * 675, 2 * 675, theta1=12, theta2=167.5,
                    linewidth=lw, color=color)

    # List of the court elements to be plotted onto the axes
    court_elements = [hoop, backboard, outer_box, inner_box,
                      restricted, top_free_throw, bottom_free_throw,
                      corner_three_a, corner_three_b, three_arc]

    # Add the court elements onto the axes
    for element in court_elements:
        ax.add_patch(element)

    return ax

def plot_scatter(made, miss, title=None):
    """
    Scatter plot of made and missed shots
    """
    plt.figure()
    draw_court()
    plt.plot(miss['x']*100, miss['y']*100, 'o', color='red', label='Missed', alpha=0.6, markeredgecolor='black', markersize=4)
    plt.plot(made['x']*100, made['y']*100, 'o', label='Made', color='green', alpha=0.6, markeredgecolor='black', markersize=4)
    plt.legend(fontsize="x-small", frameon=False)
    plt.xlim([-800, 800])
    plt.ylim([-155, 1300])
    plt.xticks([])
    plt.yticks([])
    plt.title(title)
    plt.show()
    return

fg_made_home_df = home_df[home_df['type'].isin(['2FGM', '3FGM'])]
fg_miss_home_df = home_df[home_df['type'].isin(['2FGA', '3FGA'])]

# scatter shot chart of PAOs
fig2 = plot_scatter(fg_made_home_df, fg_miss_home_df, title=teamselection)

# DATAFRAMES
statsavancees = (result[['Team_name', 'ORTG', 'DRTG', 'NetRTG', 'eFG%', 'TS%', 'AST/TO', 'OREB%', 'DREB%', 'TOV%', 'BLK%', 'STL%', 'FTAr', 'Poss/G']])
statsavancees = statsavancees.set_index('Team_name')

statsavanceesopp = (result[['Team_name', 'eFG% opp', 'TS% opp', 'AST/TO opp', 'OREB% opp', 'DREB% opp', 'TOV% opp', 'BLK% opp', 'STL% opp', 'FTAr opp', 'Poss/G opp']])
statsavanceesopp = statsavanceesopp.set_index('Team_name')

def color_rank(val):
    color = '#28B321' if val == 1 else '#35B72E' if val==2 else '#41BC3B' if val==3 else '#4EC048' if val==4 else '#5BC555' if val==5 else '#67C962' if val==6 else '#74CE6F' if val==7 else '#81D27C' if val==8 else '#8DD789' if val==9 else '#9ADB97' if val==10 else '#A6E0A4' if val==11 else '#B3E4B1' if val==12 else '#C0E9BE' if val==13 else '#CCEDCB' if val==14 else '#D9F2D8' if val==15 else '#E6F6E5' if val==16 else '#F2FBF2' if val==17 else '#FFFFFF' if val==18 else 'red'
    return f'background-color: {color}'
fourfactors = (result[['Team_name', 'eFG%', 'TOV%', 'OREB%', 'FTAr']])
fourfactors['Rk eFG%'] = fourfactors['eFG%'].rank(method='average', ascending=False)
fourfactors['Rk TOV%'] = fourfactors['TOV%'].rank(method='average', ascending=True)
fourfactors['Rk OREB%'] = fourfactors['OREB%'].rank(method='average', ascending=False)
fourfactors['Rk FTAr'] = fourfactors['FTAr'].rank(method='average', ascending=False)
fourfactors = (fourfactors[['Team_name', 'eFG%', 'Rk eFG%', 'TOV%', 'Rk TOV%', 'OREB%', 'Rk OREB%', 'FTAr', 'Rk FTAr']])
fourfactors = fourfactors.set_index('Team_name')

fourfactorsopp = (result[['Team_name', 'eFG% opp', 'TOV% opp', 'OREB% opp', 'FTAr opp']])
fourfactorsopp['Rk eFG%'] = fourfactorsopp['eFG% opp'].rank(method='average', ascending=True)
fourfactorsopp['Rk TOV%'] = fourfactorsopp['TOV% opp'].rank(method='average', ascending=False)
fourfactorsopp['Rk OREB%'] = fourfactorsopp['OREB% opp'].rank(method='average', ascending=True)
fourfactorsopp['Rk FTAr'] = fourfactorsopp['FTAr opp'].rank(method='average', ascending=True)
fourfactorsopp = (fourfactorsopp[['Team_name', 'eFG% opp', 'Rk eFG%', 'TOV% opp', 'Rk TOV%', 'OREB% opp', 'Rk OREB%', 'FTAr opp', 'Rk FTAr']])
fourfactorsopp = fourfactorsopp.set_index('Team_name')

traditionaltotal = (result[['Team_name', 'PTS', '2FGM', '2FGA', '2P%', '3FGM', '3FGA', '3P%', 'FTM', 'FTA', 'FT%', 'OREB', 'DREB', 'AST', 'STL', 'TOV', 'BLK', 'BLKA', 'PF']])
traditionaltotal = traditionaltotal.set_index('Team_name')

traditionaltotalopp = (result[['Team_name', 'PTS opp', '2FGM opp', '2FGA opp', '2P% opp', '3FGM opp', '3FGA opp', '3P% opp', 'FTM opp', 'FTA opp', 'FT% opp', 'OREB opp', 'DREB opp', 'AST opp', 'STL opp', 'TOV opp', 'BLK opp', 'BLKA opp', 'PF opp']])
traditionaltotalopp = traditionaltotalopp.set_index('Team_name')

traditionalavg = (result[['Team_name', 'PTS/G', '2PM/G', '2PA/G', '2P%', '3PM/G', '3PA/G', '3P%', 'FTM/G', 'FTA/G', 'FT%', 'OREB/G', 'DREB/G', 'TREB/G', 'AST/G', 'STL/G', 'TOV/G', 'BLK/G', 'BLKA/G', 'PF/G']])
traditionalavg = traditionalavg.set_index('Team_name')

traditionalavgopp = (result[['Team_name', 'PTS/G opp', '2PM/G opp', '2PA/G opp', '2P% opp', '3PM/G opp', '3PA/G opp', '3P% opp', 'FTM/G opp', 'FTA/G opp', 'FT% opp', 'OREB/G opp', 'DREB/G opp', 'TREB/G opp', 'AST/G opp', 'STL/G opp', 'TOV/G opp', 'BLK/G opp', 'BLKA/G opp', 'PF/G opp']])
traditionalavgopp = traditionalavgopp.set_index('Team_name')

scoring = (result[['Team_name', 'FGA% 2PT', 'FGA% 3PT', 'PTS% 2PT', 'PTS% 3PT', 'PTS% FT', 'FGM% AST', 'FGM% UAST']])
scoring = scoring.set_index('Team_name')

scoringopp = (result[['Team_name', 'FGA% 2PT opp', 'FGA% 3PT opp', 'PTS% 2PT opp', 'PTS% 3PT opp', 'PTS% FT opp', 'FGM% AST opp', 'FGM% UAST opp']])
scoringopp = scoringopp.set_index('Team_name')

# DISPLAY
row1_col1, row1_col2 = st.columns(2)
    
with row1_col1:
    st.header('Efficiency Landscape')
    st.pyplot(fig)
    st.header('Percentiles')
    st.pyplot(fig1)
    
with row1_col2:
    st.header('Statistics')
    stats = st.selectbox("",('Traditional Total', 'Traditional Average', 'Advanced Stats', 'Four Factors', 'Scoring'), label_visibility="collapsed")
    offdef = st.selectbox("",('Offense', 'Defense'), label_visibility="collapsed")
    if stats == "Four Factors" and offdef == "Offense":
        st.dataframe(fourfactors.style.format("{:.2f}").format("{:.0f}", subset=['Rk eFG%', 'Rk TOV%', 'Rk OREB%', 'Rk FTAr']).applymap(color_rank, subset=['Rk eFG%', 'Rk TOV%', 'Rk OREB%', 'Rk FTAr']))
    elif stats == "Traditional Total" and offdef == "Offense":
        st.dataframe(traditionaltotal.style.format("{:.2f}"))
    elif stats == "Traditional Average" and offdef == "Offense":
        st.dataframe(traditionalavg.style.format("{:.2f}"))
    elif stats == "Scoring" and offdef == "Offense":
        st.dataframe(scoring.style.format("{:.2f}"))
    elif stats == "Advanced Stats" and offdef == "Offense":
        st.dataframe(statsavancees.style.format("{:.2f}"))
    elif stats == "Four Factors" and offdef == "Defense":
        st.dataframe(fourfactorsopp.style.format("{:.2f}").format("{:.0f}", subset=['Rk eFG%', 'Rk TOV%', 'Rk OREB%', 'Rk FTAr']).applymap(color_rank, subset=['Rk eFG%', 'Rk TOV%', 'Rk OREB%', 'Rk FTAr']))
    elif stats == "Advanced Stats" and offdef == "Defense":
        st.dataframe(statsavanceesopp.style.format("{:.2f}"))
    elif stats == "Scoring" and offdef == "Defense":
        st.dataframe(scoringopp.style.format("{:.2f}"))
    elif stats == "Traditional Total" and offdef == "Defense":
        st.dataframe(traditionaltotalopp.style.format("{:.2f}"))
    elif stats == "Traditional Average" and offdef == "Defense":
        st.dataframe(traditionalavgopp.style.format("{:.2f}"))
    else:
        statsdf = df
    
    st.sidebar.write("##")
    st.sidebar.write("##")
    st.header('Shooting')
    shootingselect = st.selectbox("",('Shot Chart', 'Bar Chart'), label_visibility="collapsed")
    if shootingselect == "Shot Chart":
        st.pyplot(fig2)
    elif shootingselect == "Bar Chart":
        st.pyplot(fig3)
    else:
        st.write("")
    
st.write("GLOSSARY :")
st.write("ORTG : Offensive Rating / DRTG : Defensive Rating / NetRTG : Net Rating / eFG% : Effective Field Goal / TS% : True Shooting / FTAr : Free Throw rate")
st.write("FGA% 2PT : Percent of Field Goals Attempted (2 Pointers) / FGA% 3PT : Percent of Field Goals Attempted (3 Pointers) / PTS% 2PT : Percent of Points (2 Pointers) / PTS% 3PT : Percent of Points (3 Pointers) / PTS% FT : Percent of Points (Free Throws)")
st.write("FGM% AST : Percent of Point Field Goals Made Assisted / FGM% UAST : Percent of Point Field Goals Made Unassisted")


st.dataframe(team2)
st.dataframe(league2)