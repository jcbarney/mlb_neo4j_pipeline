from neo4j import GraphDatabase
import csv
user = 'neo4j'
password='password'

def create_insert_file_statement(file, node_type):
    with open('import/'+file, newline='') as f:
        reader = csv.reader(f)
        columns = next(reader)
    properties = []
    x=0
    for col in columns:
        properties.append(col+": "+f'line.{col}')
        x+=1
    property_str = ', '.join(properties)
    node_str = f"(:{node_type} {{{property_str}}})"
    return node_str

node_files = {'teams.csv': 'Team', 'leagues.csv': 'League', 'players.csv': 'Player', 'at_bat.csv': 'AtBat'}
rel_files = {'player_team_relationships.csv': {'name': 'PLAYED_FOR', 'node_a': 'Player', 'node_a_col': 'player_id', 'node_b': 'Team', 'node_b_col': 'team_id'},
'pitcher_player_relationships.csv': {'name': 'PITCHED_AT', 'node_a': 'Player', 'node_a_col': 'pitcher', 'node_b': 'AtBat', 'node_b_col': 'id'},
'batter_player_relationships.csv': {'name': 'BATTED_AT', 'node_a': 'Player', 'node_a_col': 'batter', 'node_b': 'AtBat', 'node_b_col': 'id'},
'team_league_relationships.csv': {'name': 'MEMBER_OF', 'node_a': 'Team', 'node_a_col': 'id', 'node_b': 'League', 'node_b_col': 'league'},
'batter_pitcher_relationships.csv': {'name': 'BATTED_AGAINST', 'node_a': 'Player', 'node_a_col': 'batter', 'node_b': 'Player', 'node_b_col': 'pitcher'}}

# create indices
indices=[('AtBat', 'id'), ('Player', 'id')]

driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user, password))
with driver.session() as session:
    for ix in indices:
        insert = f"""CREATE INDEX FOR (n:{ix[0]}) ON (n.{ix[1]})"""
        session.run(insert)
driver.close()


driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user, password))
batch_size=10000
with driver.session() as session:
    # add nodes
    for key in node_files.keys():
        print("uploading" + key)
        insert = f"""LOAD CSV WITH HEADERS FROM 'file:///{key}' AS line
        CALL {{
        WITH line
        CREATE {create_insert_file_statement(key, node_files[key])}
        }} IN TRANSACTIONS OF {batch_size} ROWS"""
        session.run(insert)

    #create indices for large relationship uploads
    for ix in indices:
        insert = f"""CREATE INDEX FOR (n:{ix[0]}) ON (n.{ix[1]})"""
        session.run(insert)
    
    #upload relationships
    for key in rel_files.keys():
        print("uploading" + key)
        insert = f"""LOAD CSV WITH HEADERS FROM 'file:///{key}' AS row
        CALL {{
        WITH row
        MATCH (a:{rel_files[key]['node_a']} {{id: row.{rel_files[key]['node_a_col']}}})
        USING INDEX a:{rel_files[key]['node_a']}(id)
        MATCH (b:{rel_files[key]['node_b']} {{id: row.{rel_files[key]['node_b_col']}}})
        USING INDEX b:{rel_files[key]['node_b']}(id)
        CREATE (a)-[:{rel_files[key]['name']}]->(b)}}
        IN TRANSACTIONS OF {batch_size} ROWS"""
        res=session.run(insert)
    driver.close()

