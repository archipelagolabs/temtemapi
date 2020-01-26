import json

import requests
from parsel import Selector

from temapi.commons.models import Temtem
from temapi.commons.paths import OUTPUTS_DIR
from temapi.extractor import extractors


def fetch_temtem_name_list():
    response = requests.get('https://temtem.gamepedia.com/Temtem_Species')

    sel = Selector(text=response.text)

    return sel.css('table.wikitable > tbody > tr').xpath('.//td[2]/a/@title').getall()


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
        cry=data.get('Cry'),
    )


def fetch_traits():
    print(f'Getting traits')
    response = requests.get('https://temtem.gamepedia.com/Traits')

    sel = Selector(text=response.text)
    table = sel.css('#mw-content-text > div > table > tbody > tr')

    # skip header
    for s in table[1:]:
        yield extractors.extract_trait(s)


def save(entities, filename):
    with (OUTPUTS_DIR / filename).open('w+') as f:
        json.dump([e._asdict() for e in entities], f, indent=2)


def run():
    names = fetch_temtem_name_list()

    temtems = [fetch_temtem(name) for name in names]
    for t in temtems:
        print(t)
    save(temtems, 'temtems.json')

    traits = fetch_traits()
    save(traits, 'traits.json')
