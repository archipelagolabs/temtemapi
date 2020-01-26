import json

import requests
from parsel import Selector

from temapi.commons.models import Temtem, Technique
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

technique_extractors_map = {
    'Link': extractors.extract_technique_link,
    'Name': extractors.extract_technique_name,
    'Type': extractors.extract_technique_type,
    'Class': extractors.extract_technique_class,
    'Damage': extractors.extract_technique_damage,
    'Stamina Cost': extractors.extract_technique_stamina,
    'Hold': extractors.extract_technique_hold,
    'Priority': extractors.extract_technique_priority,
    'Synergy': extractors.extract_technique_synergy,
    'Synergy Effect': extractors.extract_technique_synergy_effect,
    'Targets': extractors.extract_technique_targets
}

def fetch_techniques_links():
    print('Getting techniques')
    response = requests.get("https://temtem.gamepedia.com/Techniques")

    sel = Selector(text=response.text)
    infos = sel.css('table.wikitable > tbody > tr')
    infos.pop(0)

    return [
        technique_extractors_map['Link'](info.css('td')[0])
        for info in infos
    ]


def fetch_techniques(link : str):
    response = requests.get(f"https://temtem.gamepedia.com{link}")

    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {}
    data['Name'] = link.replace('_', ' ').replace('/', '')
    data['Description'] = ''.join(sel.xpath('//*[@id="mw-content-text"]/div/p[2]/i/text()').getall())

    for key, csel in zip(keys, infos):
        data[key] = technique_extractors_map[key](csel.css('.infobox-row-value'))

    return Technique(
        name=data['Name'],
        description=data['Description'],
        type=data['Type'],
        category=data['Class'],
        damage=data['Damage'],
        stamina_cost=data['Stamina Cost'],
        hold=data.get('Hold'),
        priority=data['Priority'],
        targets=data['Targets'],
        synergy=data.get('Synergy'),
        synergy_effect=data.get('Synergy Effect')
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
    save(temtems, 'temtems.json')

    traits = fetch_traits()
    save(traits, 'traits.json')

    links = fetch_techniques_links()
    techniques = [fetch_techniques(link) for link in links]
    save(techniques, 'techniques.json')