# -*- coding: utf-8 -*-

import diplomas.geocaching.api as gc_api
from diplomas.geocaching.geoloto_stuff import get_geoloto_cards, check_geoloto_dp
from diplomas.geocaching.regions_stuff import regions_mapping, get_region_neighbours, get_regions_diploma_criteria
from diplomas.geocaching.utils import get_card_score, \
    have_letters


def check_geoloto_for_user(user_id):
    cards = get_geoloto_cards()

    res = gc_api.get_user_finds(user_id) + gc_api.get_user_creations(user_id)

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


def check_azbuka_for_user(user_id):
    created_caches = gc_api.get_user_creations(user_id)
    res = gc_api.get_user_finds(user_id) + created_caches
    letters_to_start_with = 'абвгдежзиклмнопрстуфхцчшщэюя'
    letters_to_have = 'йыьё'
    special_letter = 'ъ'
    all_letters = sorted(list(letters_to_start_with + letters_to_have + special_letter))
    dic = {}
    for cache in sorted(res, key=lambda x: x.name):
        if cache.cache_type.lower() not in ['ms', 'tr', 'mv', 'vi', 'lu', 'ar', 're']:
            continue
        cache_name_to_check = cache.name.lower()
        if cache_name_to_check.startswith('"'):
            cache_name_to_check = cache_name_to_check[1:]
        was_cache_added = False
        if not was_cache_added:
            first_letter = cache_name_to_check[0]
            if first_letter not in dic and first_letter in letters_to_start_with:
                dic[first_letter] = cache
                all_letters.remove(first_letter)
                was_cache_added = True

        if not was_cache_added:
            letters_inside = have_letters(cache_name_to_check, letters_to_have)
            for letter in letters_inside:
                if letter not in dic:
                    dic[letter] = cache
                    was_cache_added = True
                    all_letters.remove(letter)
                    break

        if not was_cache_added:
            if special_letter not in dic:
                if special_letter in cache_name_to_check or cache in created_caches:
                    dic[special_letter] = cache
                    all_letters.remove(special_letter)
                    was_cache_added = True
    return dic, all_letters


def check_regions_for_user(user_id):
    res = gc_api.get_user_finds(user_id) + gc_api.get_user_creations(user_id)
    regions_to_caches_table = {}
    for cache in res:
        if 'Россия' not in cache.region:
            continue
        region = regions_mapping(cache.region)
        if region not in regions_to_caches_table:
            regions_to_caches_table[region] = []
        regions_to_caches_table[region].append(cache)

    number_of_caches_to_get_diploma = get_regions_diploma_criteria()

    result_table = {}
    for region in number_of_caches_to_get_diploma:
        if region in regions_to_caches_table:
            # Firstly fill neightbors
            result_table[region] = {}
            result_table[region]['neightbors'] = []
            result_table[region]['total_score'] = 0
            result_table[region]['region_max_score'] = number_of_caches_to_get_diploma[region]
            result_table[region]['max_score'] = number_of_caches_to_get_diploma[region] + len(get_region_neighbours(region))

            for neightbour in get_region_neighbours(region):
                value_to_add = (neightbour, None)
                if neightbour in regions_to_caches_table and regions_to_caches_table[neightbour]:
                    value_to_add = (neightbour, regions_to_caches_table[neightbour][0])
                    # Remove cache
                    del regions_to_caches_table[neightbour][0]
                    result_table[region]['total_score'] += 1
                result_table[region]['neightbors'].append(value_to_add)

    for region in number_of_caches_to_get_diploma:
        if region in regions_to_caches_table:
            # ANd fill the main region after
            found_in_the_region = len(regions_to_caches_table[region])
            caches_here = min(number_of_caches_to_get_diploma[region], found_in_the_region)
            caches_to_display = regions_to_caches_table[region][:caches_here]
            #Remove caches
            regions_to_caches_table[region] = regions_to_caches_table[region][caches_here:]

            result_table[region]['total_score'] += caches_here

            result_table[region]['caches'] = caches_to_display
            result_table[region]['region_score'] = caches_here
            result_table[region]['can_get'] = result_table[region]['max_score'] == result_table[region]['total_score']

    return result_table


if __name__ == '__main__':
    qqq = check_regions_for_user(4786)
    print(qqq)
    pass
