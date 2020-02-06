import json
import re
import time
from multiprocessing.pool import Pool

import requests
from parsel import Selector

from temapi.commons.models import ErrorItem, Item, Technique, Temtem
from temapi.commons.paths import OUTPUTS_DIR
from temapi.extractor import extractors

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
    'Targets': extractors.extract_technique_targets,
}

item_extractors_map = {
    'Category': extractors.extract_item_string_directly,
    'Consumable': extractors.extract_item_string_to_bool,
    'Limited Quantity': extractors.extract_item_string_to_bool,
    'Purchasable': extractors.extract_item_string_to_bool,
    'Buy Price': extractors.extract_item_string_to_int,
    'Sell Price': extractors.extract_item_string_to_int,
    'Restore Amount': extractors.extract_item_string_directly,
}


def fetch_temtem_name_list():
    print('Getting temtems')
    response = requests.get('https://temtem.gamepedia.com/Temtem_Species')
    sel = Selector(text=response.text)

    return sel.css('table.wikitable > tbody > tr').xpath('.//td[2]/a/@title').getall()


def fetch_techniques_links():
    print('Getting techniques')
    response = requests.get('https://temtem.gamepedia.com/Techniques')

    sel = Selector(text=response.text)
    infos = sel.css('table.wikitable > tbody > tr')
    infos.pop(0)

    return [technique_extractors_map['Link'](info.css('td')[0]) for info in infos]


def fetch_item_name_list():
    print('Getting items')
    response = requests.get('https://temtem.gamepedia.com/Items')
    sel = Selector(text=response.text)
    all_items = (
        sel.css('table.wikitable > tbody > tr').xpath('.//td[2]/a/@title').getall()
    )

    # TC have a different layout, so they need to be extracted separately
    return [x for x in all_items if not x.startswith('TC')]


def fetch_temtem(name):
    response = requests.get(f'https://temtem.gamepedia.com/{name}')

    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {
        'Image': extractors.extract_image(sel),
        'Status': fetch_temtem_stats(sel),
        'Evolve Info': extractors.extract_evolve_info(
            sel.xpath('//*[@id="mw-content-text"]/div/p[1]')
        ),
    }

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
        evolve_info=data.get('Evolve Info'),
        status=data.get('Status'),
        image=data.get('Image', None),
    )


def fetch_temtem_stats(sel: Selector):
    rows = sel.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr/th')

    # 2: for header skip
    keys = [
        row.css('div:first-child > b').xpath('text()').get()
        for row in rows[2:]
        if row.css('div:first-child > b').xpath('text()').get() != None
    ]
    keys.append('TOTAL')

    values = [
        row.css('div:last-child').xpath('text()').get()
        for row in rows[2:]
        if row.css('div:last-child').xpath('text()').get() != None
    ]

    return {key: value for key, value in zip(keys, values)}


def fetch_technique(link: str):
    response = requests.get(f'https://temtem.gamepedia.com{link}')

    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {
        'Name': link.replace('_', ' ').replace('/', ''),
        'Description': ''.join(
            sel.xpath('//*[@id="mw-content-text"]/div/p[2]/i/text()').getall()
        ),
    }

    for key, csel in zip(keys, infos):
        data[key] = technique_extractors_map[key](csel.css('.infobox-row-value'))

    return Technique(
        name=data['Name'],
        description=data['Description'],
        type=data['Type'],
        category=data['Class'],
        damage=data['Damage'],
        stamina_cost=data['Stamina Cost'],
        hold=data.get('Hold', 0),
        priority=data['Priority'],
        targets=data['Targets'],
        synergy=data.get('Synergy'),
        synergy_effect=data.get('Synergy Effect'),
    )


def fetch_item(name):
    response = requests.get(f'https://temtem.gamepedia.com/{name}')

    if response.status_code != 200:
        return ErrorItem(name=name, error='Page doest not exist')

    sel = Selector(text=response.text)
    infos = sel.css('table.infobox-table > tbody > tr.infobox-row')

    keys = infos.css('th.infobox-row-name > b').xpath('text()').getall()

    data = {}

    for key, csel in zip(keys, infos):
        data[key] = item_extractors_map[key](csel.css('.infobox-row-value'))

    description_selector = sel.xpath(
        '/html/body/div[2]/div[3]/div[1]/div[3]/div[4]/div/p[2]'
    )

    # shouldn't this use w3lib.html.remove_tags?
    cleaner = re.compile('<.*?>|\n')
    description = re.sub(cleaner, '', description_selector.get())

    return Item(
        name=name,
        category=data['Category'],
        consumable=data['Consumable'],
        limited_quantity=data['Limited Quantity'],
        purchasable=data.get('Purchasable', False),
        buy_price=data.get('Buy Price'),
        sell_price=data.get('Sell Price'),
        description=description,
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
        json.dump([e.dict() for e in entities], f, indent=2)


def run():
    start = time.perf_counter()
    temtem_names = fetch_temtem_name_list()
    technique_links = fetch_techniques_links()
    item_names = fetch_item_name_list()

    with Pool() as p:
        temtems = p.map(fetch_temtem, temtem_names)
        techniques = sorted(
            p.map(fetch_technique, technique_links), key=lambda t: t.name
        )
        items = p.map(fetch_item, item_names)

    save(temtems, 'temtems.json')
    save(techniques, 'techniques.json')
    save(items, 'items.json')

    traits = list(fetch_traits())
    save(traits, 'traits.json')

    print(
        f'Saved {len(temtems)} Temtems, {len(techniques)} techniques, {len(items)} items and '
        f'{len(list(traits))} traits in {time.perf_counter() - start:.2f} seconds'
    )
