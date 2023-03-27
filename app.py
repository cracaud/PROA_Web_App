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

font_dirs = ["//Users//sissigarduno//Downloads"]
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
    font_manager.fontManager.addfont(font_file)

plt.rcParams['font.family'] = "Poppins"
plt.rcParams['font.size'] = '10.6'

image = Image.open("Logos/BetclicElite.png")
st.sidebar.image(image)

# DATA
df = pd.read_csv("Data.csv")
df_shots = pd.read_csv("Shot_Data.csv")

# FILTERS
st.sidebar.header('Filters')
st.sidebar.write("Select a range of rounds :")
begin = st.sidebar.slider('First game :', 1, 34, 1)
end = st.sidebar.slider('Last game :', 1, 34, 34)
location = st.sidebar.selectbox('Home / Away :', ('All', 'Home', 'Away'))

# FILETRING DATA
df = df[df['round'].between(begin, end)]
df['Pace'] = df["2FGA"] + df["3FGA"] + 0.44*df["FTA"] - df["OREB"] + df["TOV"]

# DATA TREATMENT
# Home
hometeam = df.groupby(['home_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
hometeam = hometeam.drop(hometeam[hometeam.home_team != hometeam.team_id].index)
hometeam = hometeam.drop('team_id', axis=1)
hometeam.rename(columns={'home_team': 'Team_name'}, inplace=True)

homeopp = df.groupby(['home_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
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
awayteam = df.groupby(['away_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
                                                     'FTM' : 'sum', 'FTA' : 'sum', 'OREB' : 'sum', 'DREB' : 'sum', 'AST' : 'sum', 'STL' : 'sum', 'TOV' : 'sum',
                                                     'BLK' : 'sum', 'BLKA' : 'sum', 'PF' : 'sum'}).reset_index().rename(columns={'round':'Nb_games'})
awayteam = awayteam.drop(awayteam[awayteam.away_team != awayteam.team_id].index)
awayteam = awayteam.drop('team_id', axis=1)
awayteam.rename(columns={'away_team': 'Team_name'}, inplace=True)

awayopp = df.groupby(['away_team', 'team_id']).agg({'round': 'count', 'PTS' : 'sum', 'Pace' : 'sum', '2FGM' : 'sum', '2FGA' : 'sum', '3FGM' : 'sum', '3FGA' : 'sum',
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
teamselection = st.sidebar.selectbox('Team :',(teamname), label_visibility="collapsed")
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

# split the home and away teams, their made and missed shots
df_shots = df_shots[df_shots['round'].between(begin, end)]
#df_shots['TEAM'] = df_shots['TEAM'].str.strip()  # team id contains trailing white space
#df_shots['ID_PLAYER'] = df_shots['ID_PLAYER'].str.strip()  # player id contains trailing white space
home_df = df_shots[df_shots['team_id'] == teamselection]
fg_made_home_df = home_df[home_df['type'].isin(['2FGM', '3FGM'])]
fg_miss_home_df = home_df[home_df['type'].isin(['2FGA', '3FGA'])]

# scatter shot chart of PAOs
fig4 = plot_scatter(fg_made_home_df, fg_miss_home_df, title=teamselection)

# DATAFRAMES
statsavancees = (result[['Team_name', 'ORTG', 'DRTG', 'NetRTG', 'eFG%', 'TS%', 'AST/TO', 'OREB%', 'DREB%', 'TOV%', 'BLK%', 'STL%', 'FTAr', 'Poss/G']])
statsavancees = statsavancees.set_index('Team_name')

statsavanceesopp = (result[['Team_name', 'eFG% opp', 'TS% opp', 'AST/TO opp', 'OREB% opp', 'DREB% opp', 'TOV% opp', 'BLK% opp', 'STL% opp', 'FTAr opp', 'Poss/G opp']])
statsavanceesopp = statsavanceesopp.set_index('Team_name')

fourfactors = (result[['Team_name', 'eFG%', 'TOV%', 'OREB%', 'FTAr']])
fourfactors = fourfactors.set_index('Team_name')

fourfactorsopp = (result[['Team_name', 'eFG% opp', 'TOV% opp', 'OREB% opp', 'FTAr opp']])
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
        statsdf = fourfactors
    elif stats == "Traditional Total" and offdef == "Offense":
        statsdf = traditionaltotal
    elif stats == "Traditional Average" and offdef == "Offense":
        statsdf = traditionalavg
    elif stats == "Scoring" and offdef == "Offense":
        statsdf = scoring
    elif stats == "Advanced Stats" and offdef == "Offense":
        statsdf = statsavancees
    elif stats == "Four Factors" and offdef == "Defense":
        statsdf = fourfactorsopp
    elif stats == "Advanced Stats" and offdef == "Defense":
        statsdf = statsavanceesopp
    elif stats == "Scoring" and offdef == "Defense":
        statsdf = scoringopp
    elif stats == "Traditional Total" and offdef == "Defense":
        statsdf = traditionaltotalopp
    elif stats == "Traditional Average" and offdef == "Defense":
        statsdf = traditionalavgopp
    else:
        statsdf = df
    st.dataframe(statsdf.style.format("{:.0f}"))
    st.sidebar.write("##")
    st.sidebar.write("##")
    st.header('Shooting')
    st.pyplot(fig4)
    
st.write("GLOSSARY :")
st.write("ORTG : Offensive Rating / DRTG : Defensive Rating / NetRTG : Net Rating / eFG% : Effective Field Goal / TS% : True Shooting / FTAr : Free Throw rate")
st.write("FGA% 2PT : Percent of Field Goals Attempted (2 Pointers) / FGA% 3PT : Percent of Field Goals Attempted (3 Pointers) / PTS% 2PT : Percent of Points (2 Pointers) / PTS% 3PT : Percent of Points (3 Pointers) / PTS% FT : Percent of Points (Free Throws)")
st.write("FGM% AST : Percent of Point Field Goals Made Assisted / FGM% UAST : Percent of Point Field Goals Made Unassisted")