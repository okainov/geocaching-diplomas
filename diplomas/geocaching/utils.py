# -*- coding: utf-8 -*-


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