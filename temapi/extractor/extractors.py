import re

import parsel
from w3lib import html

from temapi.commons.models import Trait

# Temtems

re_height = re.compile(r'(\d+([.]\d+)?)cm')
re_weight = re.compile(r'(\d+([.]\d+)?)kg')
re_multiple_spaces = re.compile(r'[ \xa0]+')


def extract_id(sel: parsel.Selector):
    for c in sel.xpath('.//text()').getall():
        c = c.strip()
        if c.isdigit():
            return int(c)


def extract_types(sel: parsel.Selector):
    types = sel.xpath('.//a/@title').getall()

    return [
        t.split()[0]
        for t in types
    ]


def extract_evolves_from(sel: parsel.Selector):
    return sel.xpath('.//a/text()').get()


def extract_evolves_to(sel: parsel.Selector):
    return [sel.xpath('.//a/text()').get()]


def extract_traits(sel: parsel.Selector):
    return sel.xpath('.//a/text()').getall()


def extract_tv_yield(sel: parsel.Selector):
    return sel.xpath('.//text()').get().strip()


def extract_height(sel: parsel.Selector):
    height_str = sel.xpath('.//text()').get().strip()
    if height_str == '?':
        return None

    height = re_height.match(height_str).group(1)
    return float(height)


def extract_weight(sel: parsel.Selector):
    weight_str = sel.xpath('.//text()').get().strip()
    if weight_str == '?':
        return None

    weight = re_weight.match(weight_str).group(1)
    return float(weight)


def extract_cry(sel: parsel.Selector):
    return sel.xpath('.//span/audio/@src').get()


# Traits

def extract_effect(sel: parsel.Selector):
    s = html.remove_tags(sel.get()).strip()

    return re_multiple_spaces.sub(' ', s)


def extract_trait(sel: parsel.Selector):
    name_sel, effect_sel, learned_by_sel = sel.xpath('.//td')

    name = name_sel.xpath('.//a/text()').get()
    effect = extract_effect(effect_sel)
    learned_by = learned_by_sel.xpath('.//a/text()').getall()

    return Trait(
        name=name,
        effect=effect,
        learned_by=learned_by,
    )

# Techniques

def extract_technique_link(sel: parsel.Selector):
    return sel.css('a::attr(href)').get()


def extract_technique_name(sel: parsel.Selector):
    return sel.css('a::text').get()


def extract_technique_type(sel: parsel.Selector):
    return sel.css('a::attr(title)').get()


def extract_technique_class(sel: parsel.Selector):
    return sel.css('a::attr(title)').get()


def extract_technique_damage(sel: parsel.Selector):
    if sel.xpath('text()').get().strip() == '-' or sel.xpath('text()').get().strip() == '':
        return None
    else:
        return sel.xpath('text()').get().strip()


def extract_technique_stamina(sel: parsel.Selector):
    if sel.xpath('text()').get().strip() == '-' or sel.xpath('text()').get().strip() == '?':
        return None
    else:
        return sel.xpath('text()').get().strip()


def extract_technique_hold(sel: parsel.Selector):
    if sel.xpath('text()').get().strip() == '?' or sel.xpath('text()').get().strip() == '':
        return None
    else:
        return sel.xpath('text()').get().strip()


def extract_technique_priority(sel: parsel.Selector):
    try:
        return sel.css('a::attr(title)').get()[0]
    except TypeError:
        return None


def extract_technique_targets(sel: parsel.Selector):
    return sel.css('a::text').get()


def extract_technique_synergy(sel: parsel.Selector):
    if sel.css('a::attr(title)').get() == 'Temtem Types':
        return None
    else:
        return sel.css('a::attr(title)').get()


def extract_technique_synergy_effect(sel: parsel.Selector):
    if sel.xpath('text()').get().strip() == '-':
        return None
    else:
        return sel.xpath('text()').get().strip()