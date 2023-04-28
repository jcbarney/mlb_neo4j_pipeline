import os
import pandas as pd

# create league db
leagues = pd.DataFrame([{'id': 'NA', 'name':'National Association'},
    {'id': 'NL', 'name':'National League'},
    {'id': 'AA', 'name':'American Association'},
    {'id': 'UA', 'name':'Union Association'},
    {'id': 'PL', 'name':'Players League'},
    {'id': 'AL', 'name':'American League'},
    {'id': 'FL', 'name':'Federal League'}])
leagues.to_csv('data/leagues.csv', index=False)

#create teams db
team = pd.read_csv('data\TEAMABR.TXT', header=None)
team.columns = ['id', 'league', 'city', 'name', 'start_year', 'end_year']
#clean duplicate teams
team_counts = team.groupby(['id'])['name'].count().reset_index(drop=False)
duplicate_teams = team_counts[team_counts['name']>1]
for i in duplicate_teams['id']:
    team.loc[team['id']==i, 'start_year']=team['start_year'][team['id']==i].min()
team=team.drop_duplicates(subset='id', keep='last')
team.loc[team['league'].isnull() ,'league'] = 'NA'
team.to_csv('data/teams.csv', index=False)

#create players db
players = pd.read_csv('data\BIOFILE.TXT')
players = players.rename(columns={'PLAYERID': 'id', 'PLAY DEBUT': 'career_start', 'PLAY LASTGAME': 'career_end', 'HEIGHT': 'height', 'WEIGHT': 'weight', 'HOF': 'hof'})
players['name'] = players['FIRST'] + ' ' + players['LAST']
players['hall_of_fame'] = players['hof'].fillna('N')
players.loc[players['hall_of_fame']=='HOF', 'hall_of_fame'] = 'Y'
player_nodes = players[['id', 'name', 'career_start', 'career_end', 'height', 'weight', 'hall_of_fame']]
player_nodes=player_nodes.drop_duplicates(subset=['id'])
player_nodes[['height', 'weight']]=player_nodes[['height', 'weight']].fillna(0)
player_nodes[['name', 'career_start', 'career_end']]=player_nodes[['name', 'career_start', 'career_end']].fillna('')
player_nodes.to_csv('data/players.csv', index=False)

#create at bat db
at_bat=[]
for decade in range(1910, 2021, 10):
    files = os.listdir(f'data/{str(decade)}seve')
    for file in files:
        file = open(f'data/{str(decade)}seve/{file}', 'r')
        file = file.readlines()
        for row in file:
            row=row.strip()
            line = row.split(',')
            if line[0] == 'id':
                current = {'id': line[1]}
                previous_batter = ''
            elif line[0] == 'info':
                if line[1] == 'visteam':
                    current['visiting_team'] = line[2]
                elif line[1] == 'hometeam':
                    current['home_team'] = line[2]
                elif line[1] == 'date':
                    current['date'] = line[2]
            elif line[0] == 'start':
                #pitcher is position #1
                if (line[3]=='0') & (line[5]=='1'):
                    visiting_pitcher = line[1]
                elif (line[3]=='1') & (line[5]=='1'):
                    home_pitcher = line[1]
            elif (line[0] == 'sub'):
                if line[5] == '1':
                    if line[3]=='0':
                        visiting_pitcher = line[1]
                    elif line[3]=='1':
                        home_pitcher = line[1]
            elif line[0] == 'play':
                if previous_batter==line[3]:
                    continue
                previous_batter=line[3]
                if line[2] == '0':
                    current['batter'] = line[3]
                    current['pitcher'] = home_pitcher
                    current['batting_team'] = current['visiting_team']
                    current['pitching_team'] = current['home_team']
                else:
                    current['batter'] = line[3]
                    current['pitcher'] = visiting_pitcher
                    current['batting_team'] = current['home_team']
                    current['pitching_team'] = current['visiting_team']
                at_bat.append(current.copy())
at_bat_df = pd.DataFrame(at_bat, index=None).reset_index(drop=True)
at_bat_df['id'] = at_bat_df.index
at_bat_df.to_csv('data/at_bat.csv', index=False)

# build relationship files
players_teams = pd.concat([at_bat_df[['batter', 'batting_team']].rename(columns={'batter':'player_id', 'batting_team': 'team_id'}),at_bat_df[['pitcher', 'pitching_team']].rename(columns={'pitcher':'player_id', 'pitching_team': 'team_id'})])
players_teams=players_teams.drop_duplicates()
pitcher = at_bat_df[['id', 'pitcher']]
batter = at_bat_df[['id', 'batter']]
team_league = team[['id', 'league']]
met = at_bat_df[['batter', 'pitcher']]
players_teams.to_csv('data/player_team_relationships.csv', index=False)
pitcher.to_csv('data/pitcher_player_relationships.csv', index=False)
batter.to_csv('data/batter_player_relationships.csv', index=False)
team_league.to_csv('data/team_league_relationships.csv', index=False)
met.to_csv('data/batter_pitcher_relationships.csv', index=False)
