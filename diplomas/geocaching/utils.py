# -*- coding: utf-8 -*-

import re
from diplomas.geocaching.cache import Cache


def extract_nickname_from_webpage(page_src):
    cache_re = re.compile('<h1 class=hdr>(.+?)</h1>', flags=re.DOTALL | re.UNICODE)
    try:
        return cache_re.findall(page_src)[0]
    except:
        return None


def extract_caches_from_webpage(page_src):
    re_for_created_cache = re.compile('(?P<type>\w\w).{0,1}\.png.*?<a href=.*?pn=101&cid=(?P<id>\d+).*?blank>(?P<name>.*?)</a>.*?(?P<cdate>\d\d.\d\d.\d\d\d\d), (?P<region>.*?)[\d<]', flags=re.DOTALL | re.UNICODE)
    re_for_found_cache = re.compile('<tr><td>.*?(?P<type>\w\w).{0,1}\.png.*?<a href=.*?pn=101&cid=(?P<id>\d+).*?blank>(?P<name>.*?)</a>.*?<b>(?P<creator>.*?)</b>.*?\((?P<cdate>\d\d.\d\d.\d\d\d\d), (?P<region>.*?)\)', flags=re.DOTALL | re.UNICODE)
    if 'Созданные тайники' in page_src:
        cache_re = re_for_created_cache
    else:
        cache_re = re_for_found_cache

    caches = list()
    n_all_finds = len(cache_re.findall(page_src))
    for i, re_match in enumerate(cache_re.finditer(page_src)):

        cache_type = re_match.group('type')
        cache_id = re_match.group('id')
        cache_name = re_match.group('name')
        creation_date = re_match.group('cdate')
        region = re_match.group('region')
        if 'рейтинг' in region:
            region = region[:-10]

        try:
            cache_creator = re_match.group('creator')
        except IndexError:
            cache_creator = extract_nickname_from_webpage(page_src)

        if i % 100 == 0:
            print('%s\\%s' % (i, n_all_finds))
        current_cache = Cache(cache_id, cache_type, cache_name, cache_creator, creation_date, region)
        caches.append(current_cache)
    return caches


def get_numbers_to_cache_mapping(cache_to_number_table):
    map_numbers_to_cache = {}
    for cache in cache_to_number_table:
        for number in cache_to_number_table[cache]:
            if number not in map_numbers_to_cache:
                map_numbers_to_cache[number] = []
            map_numbers_to_cache[number].append(cache)
    return map_numbers_to_cache


def get_caches_by_type(caches_list, type):
    return [x for x in caches_list if x.cache_type == type]


def get_card_score(number_to_cache_table):
    score = 0
    for number in number_to_cache_table:
        score += len(number_to_cache_table[number])
    return score


def remove_number(cache_to_number_table, number):
    caches_to_remove = []
    for current_cache in cache_to_number_table:
        try:
            cache_to_number_table[current_cache].remove(number)
            if not cache_to_number_table[current_cache]:
                caches_to_remove.append(current_cache)
        except ValueError:
            pass
    for item_to_remove in caches_to_remove:
        del cache_to_number_table[item_to_remove]
    return cache_to_number_table


def get_cache_to_number_table(numbers_card, caches_list):
    result = {}
    for number in numbers_card:
        acceptable = [x.cache_id for x in caches_list if number in x.cache_id]
        for cache in acceptable:
            if cache not in result:
                result[cache] = []
            result[cache].append(number)
    return result