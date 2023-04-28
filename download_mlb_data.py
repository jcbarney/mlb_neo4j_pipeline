import zipfile
import urllib.request as req
import os

# create data directory if not exists
folder = 'data'
exists = os.path.exists(folder)
if exists:
    os.makedirs(folder)
# pull team data
req.urlretrieve('https://www.retrosheet.org/TEAMABR.TXT', 'data/TEAMABR.TXT')

# pull player data: https://www.retrosheet.org/biofile.htm
req.urlretrieve('https://www.retrosheet.org/BIOFILE.TXT', 'data/BIOFILE.TXT')

# pull all regular season data since 1914
for decade in range(1910, 2021, 10):
    url=f'https://www.retrosheet.org/events/{str(decade)}seve.zip'
    req.urlretrieve(url, f'data/{str(decade)}seve.zip')
    with zipfile.ZipFile(f'data/{str(decade)}seve.zip', 'r') as zipped_file:
        zipped_file.extractall(f'data/{str(decade)}seve')
    os.remove(f'data/{str(decade)}seve.zip')
    