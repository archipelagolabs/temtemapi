import re

import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup

from parsel import Selector

from temapi import extractors
from temapi.models import Temtem


def fetch_temtem_name_list():
    response = requests.get('https://temtem.gamepedia.com/Temtem_Species')

    sel = Selector(text=response.text)

    a = sel.css('table.wikitable > tbody > tr').xpath('.//td[2]/a/@title').getall()

    return a


extractors_map = {
    'No.': extractors.extract_id,
    'Type': extractors.extract_types,
    'Types': extractors.extract_types,
    'Evolves from': extractors.extract_evolves_from,
    'Evolves to': extractors.extract_evolves_to,
    'Traits': extractors.extract_traits,
    'TV Yield': extractors.extract_tv_yield,
    'Height': extractors.extract_height,
    'Weight': extractors.extract_weight,
    'Cry': extractors.extract_cry,
}


def fetch_temtem(name):
    print(f'Getting {name}')
    response = requests.get(f"https://temtem.gamepedia.com/{name}")

    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {}

    for key, csel in zip(keys, infos):
        data[key] = extractors_map[key](csel.css('.infobox-row-value'))

    return Temtem(
        id=data['No.'],
        name=name,
        types=data.get('Types') or data.get('Type'),
        evolves_from=data.get('Evolves from', None),
        evolves_to=data.get('Evolves to', []),
        traits=data['Traits'],
        tv_yield=data['TV Yield'],
        height=data['Height'],
        weight=data['Weight'],
        cry=data['Cry'],
    )


def save(temtems):
    project_root = Path(__file__).parent.parent.absolute()
    with (project_root / 'outputs/temtems.json').open('w+') as f:
        json.dump([t._asdict() for t in temtems], f)


def run():
    names = fetch_temtem_name_list()
    temtems = [fetch_temtem(name) for name in names[:5]]
    for t in temtems:
        print(t)
    save(temtems)
