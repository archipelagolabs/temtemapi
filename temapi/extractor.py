import re
import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import namedtuple

Temtem = namedtuple('Temtem', ['id', 'name', 'type', 'evolution', 'traits', 'TV'])

def sanitize_string(string):
    return re.sub(r'\n⮞⮜', '', string)

def get_temtem_name_list():
    response = requests.get("https://temtem.gamepedia.com/Temtem_Species")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    rows = soup.select('table.wikitable > tbody > tr')
    rows = rows[2:]
    
    names = []
    for row in rows:
        columns = row.find_all('td')
        name_column = columns[1]
        name = name_column.find_all('a')[1]
        names.append(name.get_attribute_list('title')[0])
        
    return names

def get_temtem(temtem_name):
    response = requests.get(f"https://temtem.gamepedia.com/{temtem_name}")

    soup = BeautifulSoup(response.content, 'html.parser')
    infos = soup.select('table.infobox-table > tbody > tr.infobox-row > td.infobox-row-value')
    
    temtem = Temtem(
        sanitize_string(infos[0].get_text()), 
        temtem_name, 
        sanitize_string(infos[1].a.get_attribute_list('title')[0]),
        sanitize_string(infos[2].get_text()),
        sanitize_string(infos[3].get_text()),
        sanitize_string(infos[4].get_text())
    )

    return temtem

def save(temtems):
    with open(Path.cwd() / Path('outputs/temtems.json'), 'w') as stream:
        stream.write(json.dumps(temtems))

def run():
    temtem_names = get_temtem_name_list()
    temtems = [get_temtem(temtem_name) for temtem_name in temtem_names[:4]]
    save(temtems)