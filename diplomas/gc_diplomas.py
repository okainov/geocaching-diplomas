# -*- coding: utf-8 -*-

import urllib.request
import re
import xml.etree.ElementTree


class Cache:
    cache_types_lookup = {'Традиционный': 'TR',
                          'Виртуальный': 'VI',
                          'Пошаговый традиционный': 'MS',
                          'Пошаговый виртуальный': 'MV'}

    def __init__(self, xml_data):
        self.cache_type = self.cache_types_lookup[xml_data.findall('type')[0].text]
        self.cache_id = xml_data.findall('id')[0].text
        self.name = xml_data.findall('name')[0].text

    def __init__(self, id, type):
        self.cache_type = type.upper()
        self.cache_id = id

    def __repr__(self):
        return '%s/%s' % (self.cache_type, self.cache_id)


def get_page_by_url(url):
    r = urllib.request.urlopen(url)
    bytes_str = r.read()
    return bytes_str.decode('cp1251')

def get_cache_info(cache_id):
    page_src = get_page_by_url('http://www.geocaching.su/site/api.php?rtype=2&cid=%s&istr=ems' % cache_id).read()
    root = xml.etree.ElementTree.fromstring(page_src)
    return Cache(root)


def get_user_finds(user_id, detailed=False):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=2&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src, detailed)


def get_user_creations(user_id, detailed=False):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=1&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src, detailed)


def get_user_nickname(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=1&uid=%s" % user_id)
    return extract_nickname_from_webpage(page_src)


def extract_nickname_from_webpage(page_src):
    cache_re = re.compile('<h1 class=hdr>(.+?)</h1>', flags=re.DOTALL | re.UNICODE)
    try:
        return cache_re.findall(page_src)[0]
    except:
        return None


def extract_caches_from_webpage(page_src, detailed=False):
    cache_re = re.compile('(\w\w).{0,1}\.png.*?<a href=.*?pn=101&cid=(\d+)', flags=re.DOTALL | re.UNICODE)
    caches = []
    n_all_finds = len(cache_re.findall(page_src))
    for i, cache_result in enumerate(cache_re.findall(page_src)):
        cache_type, cache_id = cache_result
        if i % 100 == 0:
            print('%s\\%s' % (i, n_all_finds))
        if detailed:
            try:
                current_cache = get_cache_info(cache_id)
            except:
                print(cache_id)
                pass
        else:
            current_cache = Cache(cache_id, cache_type)
        caches.append(current_cache)
    return caches


def get_caches_by_type(caches_list, type):
    return [x for x in caches_list if x.cache_type == type]


def get_card_score(number_to_cache_table):
    score = 0
    for number in number_to_cache_table:
        score += len(number_to_cache_table[number])
    return score


def check_geoloto_dp(caches_list, numbers_card):
    dic = {}
    cache_to_number_table = {}
    for cache_type in ['TR', 'VI', 'MS', 'MV']:
        caches_to_process = get_caches_by_type(caches_list, cache_type)
        cache_to_number_table = get_cache_to_number_table(numbers_card, caches_to_process)
        get_cache_to_number_table_with_simple_ones_heuristic(cache_type, cache_to_number_table, dic)
        get_cache_to_number_table_with_simple_singleton_two(cache_type, cache_to_number_table, dic)
        get_cache_to_number_table_with_two_equal_pairs(cache_type, cache_to_number_table, dic)
    return dic, cache_to_number_table


def get_cache_to_number_table_with_simple_singleton_two(cache_type, cache_to_number_table, resulted_dict):
    # Check if there is only one cache in table an it could be paired
    # with two numbers -> then select first number and pair
    # Works with {'11538': ['11', '53']} as well as  with
    # {'6576': ['57', '65'], '11538': ['11', '53']}

    restart_needed = True
    while restart_needed and cache_to_number_table:
        map_numbers_to_cache = get_numbers_to_cache_mapping(cache_to_number_table)
        restart_needed = False
        for number in sorted(map_numbers_to_cache):
            if len(map_numbers_to_cache[number]) == 1:
                cache = map_numbers_to_cache[number][0]
                if number not in resulted_dict:
                    resulted_dict[number] = {}
                resulted_dict[number][cache_type] = cache

                del cache_to_number_table[cache]
                restart_needed = True
                break
    return resulted_dict


def get_cache_to_number_table_with_two_equal_pairs(cache_type, cache_to_number_table, resulted_dict):
    # {'1212': ['1', '2'], '2121': ['1', '2']}

    restart_needed = True
    while restart_needed and cache_to_number_table:
        map_numbers_to_cache = get_numbers_to_cache_mapping(cache_to_number_table)
        restart_needed = False
        for number in sorted(map_numbers_to_cache):
            if len(map_numbers_to_cache[number]) == 2:
                map_numbers_to_cache[number] = sorted(map_numbers_to_cache[number])
                cache_a = map_numbers_to_cache[number][0]
                cache_b = map_numbers_to_cache[number][1]
                caches_numbers = set(cache_to_number_table[cache_a] + cache_to_number_table[cache_b])
                if len(caches_numbers) == 2:
                    caches_numbers.remove(number)
                    number_b = list(caches_numbers)[0]

                    if number not in resulted_dict:
                        resulted_dict[number] = {}
                    if number_b not in resulted_dict:
                        resulted_dict[number_b] = {}
                    resulted_dict[number][cache_type] = cache_a
                    resulted_dict[number_b][cache_type] = cache_b

                    del cache_to_number_table[cache_a]
                    del cache_to_number_table[cache_b]
                    restart_needed = True
                    break
    return resulted_dict


def get_numbers_to_cache_mapping(cache_to_number_table):
    map_numbers_to_cache = {}
    for cache in cache_to_number_table:
        for number in cache_to_number_table[cache]:
            if number not in map_numbers_to_cache:
                map_numbers_to_cache[number] = []
            map_numbers_to_cache[number].append(cache)
    return map_numbers_to_cache


def get_cache_to_number_table_with_simple_ones_heuristic(cache_type, cache_to_number_table, resulted_dict):
    restart_needed = True
    while restart_needed:
        restart_needed = False
        for cache in cache_to_number_table:
            if len(cache_to_number_table[cache]) == 1:
                number = cache_to_number_table[cache][0]
                if number not in resulted_dict:
                    resulted_dict[number] = {}
                resulted_dict[number][cache_type] = cache

                cache_to_number_table = remove_number(cache_to_number_table, number)
                restart_needed = True
                break
    return resulted_dict


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


def get_user_result(user_id):
    cards = [
        list(map(str, [6, 11, 20, 28, 32, 34, 45, 47, 51, 53, 63, 70, 77, 86, 89])),
        list(map(str, [2, 9, 12, 17, 21, 24, 38, 43, 46, 59, 60, 65, 73, 81, 87])),
        list(map(str, [3, 14, 16, 25, 37, 39, 41, 50, 57, 61, 62, 74, 78, 85, 90])),
        list(map(str, [1, 5, 19, 23, 33, 36, 48, 52, 54, 66, 67, 71, 72, 80, 88])),
        list(map(str, [8, 15, 18, 22, 26, 35, 40, 49, 55, 58, 64, 69, 76, 82, 89])),
        list(map(str, [4, 7, 10, 13, 27, 29, 30, 31, 42, 44, 56, 68, 75, 79, 83])),
        list(map(str, [7, 9, 15, 18, 21, 26, 33, 45, 47, 59, 62, 64, 78, 84, 89])),
        list(map(str, [5, 19, 22, 28, 30, 37, 44, 46, 54, 58, 69, 71, 75, 82, 90])),
        list(map(str, [6, 8, 10, 17, 24, 32, 35, 43, 52, 55, 61, 68, 70, 83, 86])),
        list(map(str, [4, 11, 16, 29, 38, 40, 42, 53, 57, 65, 67, 73, 74, 80, 87])),
        list(map(str, [2, 13, 14, 20, 27, 31, 39, 48, 51, 56, 60, 77, 79, 85, 88])),
        list(map(str, [1, 3, 12, 23, 25, 34, 36, 41, 49, 50, 63, 66, 72, 76, 81])),
        list(map(str, [7, 15, 19, 20, 22, 36, 38, 47, 50, 54, 69, 76, 78, 84, 90])),
        list(map(str, [2, 13, 16, 29, 32, 35, 43, 49, 51, 57, 60, 66, 79, 83, 86])),
        list(map(str, [1, 9, 14, 25, 27, 33, 44, 46, 59, 62, 67, 71, 77, 80, 87])),
        list(map(str, [4, 8, 10, 12, 21, 26, 39, 41, 45, 53, 61, 73, 75, 81, 88])),
        list(map(str, [5, 17, 24, 31, 37, 40, 42, 55, 58, 63, 68, 70, 74, 82, 89])),
        list(map(str, [3, 6, 11, 18, 23, 28, 30, 34, 48, 52, 56, 64, 65, 72, 85])),
        list(map(str, [4, 10, 18, 21, 26, 32, 34, 40, 45, 51, 57, 69, 72, 80, 89])),
        list(map(str, [6, 8, 14, 28, 20, 39, 41, 46, 55, 62, 65, 70, 79, 82, 90])),
        list(map(str, [1, 16, 19, 24, 33, 38, 48, 50, 54, 61, 66, 73, 75, 81, 84])),
        list(map(str, [7, 9, 11, 23, 31, 36, 44, 47, 59, 60, 63, 71, 74, 83, 85])),
        list(map(str, [2, 5, 13, 17, 25, 29, 35, 37, 43, 52, 56, 64, 68, 78, 86])),
        list(map(str, [3, 12, 15, 22, 27, 30, 42, 49, 53, 58, 67, 76, 77, 87, 88])),
    ]

    res = get_user_finds(user_id) + get_user_creations(user_id)

    BEST_SCORE = 15 * 4
    max_score = -1
    max_tables = []
    max_cards = []
    max_cache_to_number_tables = []

    for i, card in enumerate(cards, 1):
        current_table, cache_to_number_table = check_geoloto_dp(res, card)
        current_score = get_card_score(current_table)
        if current_score > max_score:
            max_score = current_score
            max_tables = [sorted(current_table.items(), key=lambda x: int(x[0]))]
            max_cards = [i]
            max_cache_to_number_tables = [cache_to_number_table]
        elif current_score == max_score:
            max_cache_to_number_tables.append(cache_to_number_table)
            max_cards.append(i)
            max_tables.append(sorted(current_table.items(), key=lambda x: int(x[0])))
    print('Best score: %s with cards %s' % (max_score, str(max_cards)))

    return max_score, zip(max_cards, max_tables), len(res)


if __name__ == '__main__':
    qqq = get_user_nickname(20222)
    print(qqq)
    pass
