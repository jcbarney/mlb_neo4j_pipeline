# mlb_neo4j_pipeline

Final project for INFO I535 Management, Access, and Use of Big and Complex Data.

Pipeline of MLB event data into a graph database for efficient queries across relationships.

Resources used:
- Cloud computing platform with a Ubuntu 22.04 instance
- 60GB root disk
- 8 CPUs

Steps to set up a Neo4j database instance and create a visualization:

- Clone the git repository
- Run “CURRENT_UID=root docker-compose up” to create a new Neo4j instance
- In another CLI run the following as superuser:
-  pip install -r requirements.txt
-  download_mlb_data.py
-  build_data_files.py
-  sudo python3 upload_data.py
-  describe_and_visualize.py: this will print some Major League Baseball statistics and create a visualizations showing a version of the shortest path of players who have met on the plate from Mike Trout, a player today, to Babe Ruth. This can be found in your current directory in a file called shortest_path.html and can be viewed in an internet browser
- Run “docker-compose down”

MLB data: The information used here was obtained free of
charge from and is copyrighted by Retrosheet.  Interested
parties may contact Retrosheet at 20 Sunset Rd.,
Newark, DE 19711.
