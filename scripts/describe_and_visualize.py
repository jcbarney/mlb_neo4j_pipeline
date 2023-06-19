#query
from neo4j import GraphDatabase
from pyvis.network import Network

user = 'neo4j'
password='password'
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(user, password))
with driver.session() as session:
    #print some stats from the data
    query = f"""MATCH (p:AtBat)
        WHERE p.pitcher = 'schem001'
        RETURN count(p)"""
    res =session.run(query)
    records = res.data()[0]['count(p)']
    print("Max Scherzer has pitched during " + str(records) + ' plate appearances')
    query = f"""MATCH (p:AtBat)
        WHERE p.batter = 'schem001'
        RETURN count(p)"""
    res =session.run(query)
    records = res.data()[0]['count(p)']
    print("Max Scherzer has batted during " + str(records) + ' plate appearances')
    query = f"""MATCH (p:Player)-[:PLAYED_FOR]-(t:Team)
        WHERE p.id = 'schem001'
        RETURN t"""
    res =session.run(query)
    records = res.data()
    print("Max Scherzer has played for the following teams: " + ', '.join([records[i]['t']['name'] for i in range(len(records))]))
    query = f"""MATCH (p:Player)
                RETURN count(p)"""
    res =session.run(query)
    records = res.data()[0]['count(p)']
    print("Number of players from 1914-2022: " + str(records))
    query = f"""MATCH (p:AtBat)
                RETURN count(p)"""
    res =session.run(query)
    records = res.data()[0]['count(p)']
    print("Number of plate appearances from any player from 1914-2022: " + str(records))

    query = f"""MATCH (t:Team)
        RETURN t.name, duration.between(date(t.start_year+'-01-01'), date(t.end_year+'-01-01')) AS difference
        ORDER BY difference DESC
        LIMIT 1"""
    res = session.run(query)
    records = res.single()
    print("Longest existing team: " + str(records[0]) + ' for ' + str(int(records.get('difference').months/12)) + ' years')
    #get the shortest path between Babe Ruth and Mike Trout
    query = f"""MATCH (start:Player {{id: 'ruthb101'}}), (end:Player {{id: 'troum001'}})
            MATCH p = shortestPath((start)-[:BATTED_AGAINST*]-(end))
            RETURN p"""
    res =session.run(query)
    records = res.single()[0]
driver.close()

# create a viz of the shortest path results
net = Network(height="750px", width="100%")
for node in records.nodes:
    net.add_node(node.element_id, label=node.get('name'), title='Player')
for rel in records.relationships:
    net.add_edge(rel.start_node.element_id, rel.end_node.element_id)
net.save_graph("shortest_path.html")
