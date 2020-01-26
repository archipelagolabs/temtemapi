import json
import re
import time
from multiprocessing.pool import Pool

import requests
from parsel import Selector
from typing import NamedTuple

from temapi.commons.models import Temtem, Technique
from temapi.commons.paths import OUTPUTS_DIR
from temapi.extractor import extractors

class Item(NamedTuple):
    name: str
    category: str
    consumable: bool
    limited_quantity: bool
    purchasable: bool
    buy_price: int
    sell_price: int
    description: str

class Medicine(Item):
    restore_amount: str

class ErrorItem(NamedTuple):
    name: str
    error: str

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

# Items

item_extractors_map = {
    'Category': extractors.extract_item_string_directly,
    'Consumable': extractors.extract_item_string_to_bool,
    'Limited Quantity': extractors.extract_item_string_to_bool,
    'Purchasable': extractors.extract_item_string_to_bool,
    'Buy Price': extractors.extract_item_string_to_int,
    'Sell Price': extractors.extract_item_string_to_int,
    'Restore Amount': extractors.extract_item_string_directly,
}

def fetch_item_name_list():
    response = requests.get('https://temtem.gamepedia.com/Items')

    sel = Selector(text=response.text)
    
    all_items = sel.css('table.wikitable > tbody > tr').xpath('.//td[2]/a/@title').getall()

    # TC have a different layout, so they need to be extracted separately
    items_without_courses = [x for x in all_items if not x.startswith('TC')]

    return items_without_courses

def fetch_item(name):
    print(f'Getting {name}')
    response = requests.get(f"https://temtem.gamepedia.com/{name}")
    if response.status_code != 200:
        print('Page does not exist')
        return
    
    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {}

    for key, csel in zip(keys, infos):
        data[key] = item_extractors_map[key](csel.css('.infobox-row-value'))
    
    if not "Buy Price" in data:
        data['Buy Price'] = None
    if not "Sell Price" in data:
        data['Sell Price'] = None
    if not "Purchasable" in data:
        data['Purchasable'] = False
    
    description_selector = sel.xpath('/html/body/div[2]/div[3]/div[1]/div[3]/div[4]/div/p[2]')
    
    cleaner = re.compile('<.*?>|\n')
    description = re.sub(cleaner, '', description_selector.get())
    
    
    return Item(
        name=name,
        category=data['Category'],
        consumable=data['Consumable'],
        limited_quantity=data['Limited Quantity'],
        purchasable=data.get('Purchasable'),
        buy_price=data.get('Buy Price'),
        sell_price=data.get('Sell Price'),
        description=description,
    )


def save(entities, filename):
    with (OUTPUTS_DIR / filename).open('w+') as f:
        json.dump([e.dict() for e in entities], f, indent=2)


def run():
    start = time.perf_counter()
    names = fetch_temtem_name_list()
    
    with Pool() as p:
        temtems = p.map(fetch_temtem, names)
      
    save(temtems, 'temtems.json')
    print(f'Saved {len(temtems)} Temtems in {time.perf_counter() - start:.2f} seconds')

    traits = fetch_traits()
    save(traits, 'traits.json')

    names = fetch_item_name_list()
    items = []
    for name in names:
        item = fetch_item(name)
        if item:
            items.append(item)

    save(items, 'items.json')

    links = fetch_techniques_links()
    techniques = [fetch_techniques(link) for link in links]
    save(techniques, 'techniques.json')
