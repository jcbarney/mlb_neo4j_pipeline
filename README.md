# mlb_neo4j_pipeline
Pipeline of MLB event data into a graph database for efficient queries across relationships. Final project for INFO I535 Management, Access, and Use of Big and Complex Data.

The information used here was obtained free of
charge from and is copyrighted by Retrosheet.  Interested
parties may contact Retrosheet at 20 Sunset Rd.,
Newark, DE 19711.

Steps to create a Neo4j database instance and create a visualization:

- Log into Jetstream2 (or any other Linux based cloud computing platform with modifications to the instructions) and create a new Ubuntu 22.04 instance with a 60GB root disk and 8 CPUs
- Open the the web desktop and navigate to your terminal
- Navigate into your documents directory by running “cd Documents”
- Clone the git repository that contains the files we will be using by running “git clone https://github.com/jcbarney/mlb_neo4j_pipeline.git”
- Navigate into the local git repository by running “cd mlb_neo4j_pipeline”
- Run “CURRENT_UID=root docker-compose up”. This will create a new Neo4j instance with the username “neo4j” and password “password”. To see the - - database settings you may see the docker-compose.yaml file
- Keeping this CLI open, open a new command line window
- Again navigate into the git repository “cd Documents/mlb_neo4j_pipeline”
- Run “sudo pip install pandas neo4j”
- Run “sudo python3 download_mlb_data.py”. This will take some time as it will be downloading and unzipping almost 14 GB of data onto your virtual machine. Once it’s done you should have a data directory containing subdirectories with data from 1914 to 2022 and two text files called TEAMABR and BIOFILE
- Run “sudo python3 build_data_files.py”. This will also take some time as it is parsing the downloaded files and creating new files in the format we will need to make database uploads
- Run “sudo python3 upload_data.py”. This will take some time as it is uploading tens of millions of nodes and relationships into our database
- Run “sudo python3 describe_and_visualize.py”. This will print some Major League Baseball statistics and create a visualizations showing a version of the shortest path of players who have met on the plate from Mike Trout, a player today, to Babe Ruth. This can be found in your current directory in a file called shortest_path.html and can be viewed in an internet browser
- Run “docker-compose down”
- Once you are done exploring and/or exporting your results, make sure to shelve your virtual machine if you would like to use it again later, otherwise be sure to delete it
