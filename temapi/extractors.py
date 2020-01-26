import re

import parsel

re_height = re.compile(r'(\d+)cm')
re_weight = re.compile(r'(\d+)kg')


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
    height_str = sel.xpath('.//text()').get()
    height = re_height.match(height_str).group(1)
    return int(height)


def extract_weight(sel: parsel.Selector):
    weight_str = sel.xpath('.//text()').get()
    weight = re_weight.match(weight_str).group(1)
    return int(weight)


def extract_cry(sel: parsel.Selector):
    return sel.xpath('.//span/audio/@src').get()
