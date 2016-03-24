# -*- coding: utf-8 -*-

import diplomas.geocaching.api as gc_api
from diplomas.geocaching.utils import remove_number, get_cache_to_number_table, get_caches_by_type, get_card_score, \
    get_numbers_to_cache_mapping


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


def get_geoloto_cards():
    cards = [['6', '11', '20', '28', '32', '34', '45', '47', '51', '53', '63', '70', '77', '86', '89'],
             ['2', '9', '12', '17', '21', '24', '38', '43', '46', '59', '60', '65', '73', '81', '87'],
             ['3', '14', '16', '25', '37', '39', '41', '50', '57', '61', '62', '74', '78', '85', '90'],
             ['1', '5', '19', '23', '33', '36', '48', '52', '54', '66', '67', '71', '72', '80', '88'],
             ['8', '15', '18', '22', '26', '35', '40', '49', '55', '58', '64', '69', '76', '82', '89'],
             ['4', '7', '10', '13', '27', '29', '30', '31', '42', '44', '56', '68', '75', '79', '83'],
             ['7', '9', '15', '18', '21', '26', '33', '45', '47', '59', '62', '64', '78', '84', '89'],
             ['5', '19', '22', '28', '30', '37', '44', '46', '54', '58', '69', '71', '75', '82', '90'],
             ['6', '8', '10', '17', '24', '32', '35', '43', '52', '55', '61', '68', '70', '83', '86'],
             ['4', '11', '16', '29', '38', '40', '42', '53', '57', '65', '67', '73', '74', '80', '87'],
             ['2', '13', '14', '20', '27', '31', '39', '48', '51', '56', '60', '77', '79', '85', '88'],
             ['1', '3', '12', '23', '25', '34', '36', '41', '49', '50', '63', '66', '72', '76', '81'],
             ['7', '15', '19', '20', '22', '36', '38', '47', '50', '54', '69', '76', '78', '84', '90'],
             ['2', '13', '16', '29', '32', '35', '43', '49', '51', '57', '60', '66', '79', '83', '86'],
             ['1', '9', '14', '25', '27', '33', '44', '46', '59', '62', '67', '71', '77', '80', '87'],
             ['4', '8', '10', '12', '21', '26', '39', '41', '45', '53', '61', '73', '75', '81', '88'],
             ['5', '17', '24', '31', '37', '40', '42', '55', '58', '63', '68', '70', '74', '82', '89'],
             ['3', '6', '11', '18', '23', '28', '30', '34', '48', '52', '56', '64', '65', '72', '85'],
             ['4', '10', '18', '21', '26', '32', '34', '40', '45', '51', '57', '69', '72', '80', '89'],
             ['6', '8', '14', '28', '20', '39', '41', '46', '55', '62', '65', '70', '79', '82', '90'],
             ['1', '16', '19', '24', '33', '38', '48', '50', '54', '61', '66', '73', '75', '81', '84'],
             ['7', '9', '11', '23', '31', '36', '44', '47', '59', '60', '63', '71', '74', '83', '85'],
             ['2', '5', '13', '17', '25', '29', '35', '37', '43', '52', '56', '64', '68', '78', '86'],
             ['3', '12', '15', '22', '27', '30', '42', '49', '53', '58', '67', '76', '77', '87', '88']]
    return cards


def have_letters(name, letters_to_have):
    result_letters = []
    for letter in letters_to_have:
        if letter in name:
            result_letters.append(letter)
    return result_letters


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


def regions_mapping(region):
    if region in ['Россия, Ямало-Ненецкий авт. окр.', 'Россия, Ханты-Мансийский авт. окр.', 'Россия, Тюменская обл.']:
        return 'Россия, Тюменская обл.'
    elif region in ['Россия, Ненецкий авт. окр.', 'Россия, Архангельская обл.']:
        return 'Россия, Архангельская обл.'
    else:
        return region


def get_region_neighbours(region):
    ########################################## ЦФО ##########################################
    if region == 'Россия, Белгородская обл.':
        return ['Россия, Воронежская обл.', 'Россия, Курская обл.']
    elif region == 'Россия, Брянская обл.':
        return ['Россия, Калужская обл.', 'Россия, Курская обл.', 'Россия, Орловская обл.', 'Россия, Смоленская обл.']
    elif region == 'Россия, Владимирская обл.':
        return ['Россия, Ивановская обл.', 'Россия, Московская обл.', 'Россия, Нижегородская обл.',
                'Россия, Рязанская обл.',
                'Россия, Ярославская обл.']
    elif region == 'Россия, Воронежская обл.':
        return ['Россия, Белгородская обл.', 'Россия, Волгоградская обл.', 'Россия, Курская обл.',
                'Россия, Липецкая обл.',
                'Россия, Ростовская обл.', 'Россия, Саратовская обл.', 'Россия, Тамбовская обл.']
    elif region == 'Россия, Ивановская обл.':
        return ['Россия, Владимирская обл.', 'Россия, Костромская обл.', 'Россия, Нижегородская обл.',
                'Россия, Ярославская обл.']
    elif region == 'Россия, Калужская обл.':
        return ['Россия, Брянская обл.', 'Россия, Московская обл.', 'Россия, Орловская обл.', 'Россия, Смоленская обл.',
                'Россия, Тульская обл.']
    elif region == 'Россия, Костромская обл.':
        return ['Россия, Вологодская обл.', 'Россия, Ивановская обл.', 'Россия, Кировская обл.',
                'Россия, Нижегородская обл.', 'Россия, Ярославская обл.']
    elif region == 'Россия, Курская обл.':
        return ['Россия, Белгородская обл.', 'Россия, Брянская обл.', 'Россия, Воронежская обл.',
                'Россия, Липецкая обл.',
                'Россия, Орловская обл.']
    elif region == 'Россия, Липецкая обл.':
        return ['Россия, Воронежская обл.', 'Россия, Курская обл.', 'Россия, Орловская обл.',
                'Россия, Рязанская обл.', 'Россия, Тамбовская обл.', 'Россия, Тульская обл.']
    elif region == 'Россия, Московская обл.':
        return ['Россия, Владимирская обл.', 'Россия, Калужская обл.', 'Россия, Рязанская обл.',
                'Россия, Смоленская обл.',
                'Россия, Тульская обл.', 'Россия, Тверская обл.', 'Россия, Ярославская обл.']
    elif region == 'Россия, Орловская обл.':
        return ['Россия, Брянская обл.', 'Россия, Калужская обл.', 'Россия, Курская обл.',
                'Россия, Липецкая обл.', 'Россия, Тульская обл.']
    elif region == 'Россия, Рязанская обл.':
        return ['Россия, Мордовия респ.', 'Россия, Владимирская обл.', 'Россия, Липецкая обл.',
                'Россия, Московская обл.', 'Россия, Тульская обл.',
                'Россия, Нижегородская обл.', 'Россия, Пензенская обл.', 'Россия, Тамбовская обл.', ]
    elif region == 'Россия, Смоленская обл.':
        return ['Россия, Брянская обл.', 'Россия, Калужская обл.', 'Россия, Московская обл.',
                'Россия, Псковская обл.', 'Россия, Тверская обл.']
    elif region == 'Россия, Тамбовская обл.':
        return ['Россия, Воронежская обл.', 'Россия, Липецкая обл.', 'Россия, Пензенская обл.',
                'Россия, Рязанская обл.', 'Россия, Саратовская обл.']
    elif region == 'Россия, Тверская обл.':
        return ['Россия, Вологодская обл.', 'Россия, Московская обл.', 'Россия, Новгородская обл.',
                'Россия, Псковская обл.', 'Россия, Смоленская обл.', 'Россия, Ярославская обл.', ]
    elif region == 'Россия, Тульская обл.':
        return ['Россия, Калужская обл.', 'Россия, Липецкая обл.', 'Россия, Московская обл.',
                'Россия, Орловская обл.', 'Россия, Рязанская обл.', ]
    elif region == 'Россия, Ярославская обл.':
        return ['Россия, Владимирская обл.', 'Россия, Вологодская обл.', 'Россия, Ивановская обл.',
                'Россия, Костромская обл.', 'Россия, Московская обл.', 'Россия, Тверская обл.']
    ########################################## СЗФО #####################################
    elif region == 'Россия, Карелия респ.':
        return ['Россия, Архангельская обл.', 'Россия, Вологодская обл.', 'Россия, Ленинградская обл.',
                'Россия, Мурманская обл.']
    elif region == 'Россия, Коми респ.':
        return ['Россия, Пермский край', 'Россия, Архангельская обл.',
                'Россия, Кировская обл.', 'Россия, Свердловская обл.', 'Россия, Тюменская обл.', ]
    elif region == 'Россия, Архангельская обл.':
        return ['Россия, Карелия респ.', 'Россия, Коми респ.', 'Россия, Вологодская обл.',
                'Россия, Кировская обл.', 'Россия, Тюменская обл.', ]
    elif region == 'Россия, Вологодская обл.':
        return ['Россия, Карелия респ.', 'Россия, Архангельская обл.', 'Россия, Кировская обл.',
                'Россия, Костромская обл.', 'Россия, Ленинградская обл.', 'Россия, Новгородская обл.',
                'Россия, Тверская обл.', 'Россия, Ярославская обл.', ]
    elif region == 'Россия, Калининградская обл.':
        return []
    elif region == 'Россия, Ленинградская обл.':
        return ['Россия, Карелия респ.', 'Россия, Вологодская обл.',
                'Россия, Новгородская обл.', 'Россия, Псковская обл.']
    elif region == 'Россия, Мурманская обл.':
        return ['Россия, Карелия респ.']
    elif region == 'Россия, Новгородская обл.':
        return ['Россия, Вологодская обл.', 'Россия, Ленинградская обл.', 'Россия, Псковская обл.',
                'Россия, Тверская обл.']
    elif region == 'Россия, Псковская обл.':
        return ['Россия, Ленинградская обл.', 'Россия, Новгородская обл.', 'Россия, Смоленская обл.',
                'Россия, Тверская обл.']
    ########################################## ПФО ##########################################
    elif region == 'Россия, Башкортостан респ.':
        return ['Россия, Татарстан респ.', 'Россия, Удмуртская респ.', 'Россия, Пермский край',
                'Россия, Оренбургская обл.', 'Россия, Свердловская обл.', 'Россия, Челябинская обл.', ]
    elif region == 'Россия, Марий Эл респ.':
        return ['Россия, Татарстан респ.', 'Россия, Чувашская респ.',
                'Россия, Кировская обл.', 'Россия, Нижегородская обл.', ]
    elif region == 'Россия, Мордовия респ.':
        return ['Россия, Чувашская респ.', 'Россия, Нижегородская обл.', 'Россия, Пензенская обл.',
                'Россия, Рязанская обл.', 'Россия, Ульяновская обл.']
    elif region == 'Россия, Татарстан респ.':
        return ['Россия, Башкортостан респ.', 'Россия, Марий Эл респ.', 'Россия, Удмуртская респ.',
                'Россия, Чувашская респ.', 'Россия, Кировская обл.', 'Россия, Оренбургская обл.',
                'Россия, Самарская обл.', 'Россия, Ульяновская обл.']
    elif region == 'Россия, Удмуртская респ.':
        return ['Россия, Башкортостан респ.', 'Россия, Татарстан респ.', 'Россия, Пермский край',
                'Россия, Кировская обл.']
    elif region == 'Россия, Чувашская респ.':
        return ['Россия, Марий Эл респ.', 'Россия, Мордовия респ.', 'Россия, Татарстан респ.',
                'Россия, Нижегородская обл.', 'Россия, Ульяновская обл.']
    elif region == 'Россия, Пермский край':
        return ['Россия, Башкортостан респ.', 'Россия, Коми респ.', 'Россия, Удмуртская респ.',
                'Россия, Кировская обл.', 'Россия, Свердловская обл.']
    elif region == 'Россия, Кировская обл.':
        return ['Россия, Коми респ.', 'Россия, Марий Эл респ.', 'Россия, Татарстан респ.',
                'Россия, Удмуртская респ.', 'Россия, Пермский край', 'Россия, Архангельская обл.',
                'Россия, Вологодская обл.', 'Россия, Костромская обл.', 'Россия, Нижегородская обл.', ]
    elif region == 'Россия, Нижегородская обл.':
        return ['Россия, Марий Эл респ.', 'Россия, Мордовия респ.', 'Россия, Чувашская респ.',
                'Россия, Владимирская обл.', 'Россия, Ивановская обл.', 'Россия, Кировская обл.',
                'Россия, Костромская обл.', 'Россия, Рязанская обл.']


def check_regions_for_user(user_id):
    res = gc_api.get_user_finds(user_id) + gc_api.get_user_creations(user_id)
    # gc_api.get_user_finds(user_id) + gc_api.get_user_creations(user_id) + \
    # gc_api.get_user_finds(20222) + gc_api.get_user_creations(20222) +  \
    # gc_api.get_user_finds(18550) + gc_api.get_user_creations(18550) + \
    # gc_api.get_user_finds(36762) + gc_api.get_user_creations(36762) + \
    # gc_api.get_user_finds(35931) + gc_api.get_user_creations(35931) + \
    # gc_api.get_user_finds(21766) + gc_api.get_user_creations(21766) + \
    # gc_api.get_user_finds(68451) + gc_api.get_user_creations(68451) + \
    # gc_api.get_user_finds(10940) + gc_api.get_user_creations(10940) + \
    # gc_api.get_user_finds(978) + gc_api.get_user_creations(978) + \
    # gc_api.get_user_finds(72375) + gc_api.get_user_creations(72375) + \
    # gc_api.get_user_finds(7909) + gc_api.get_user_creations(7909) + \
    # gc_api.get_user_finds(20074) + gc_api.get_user_creations(20074) + \
    # gc_api.get_user_finds(14658) + gc_api.get_user_creations(14658) + \
    # gc_api.get_user_finds(25156) + gc_api.get_user_creations(25156)
    regions_to_caches_table = {}
    for cache in res:
        if 'Россия' not in cache.region:
            continue
        region = regions_mapping(cache.region)
        if region not in regions_to_caches_table:
            regions_to_caches_table[region] = []
        regions_to_caches_table[region].append(cache)

    number_of_caches_to_get_diploma = {
        'Россия, Адыгея респ.': 4,
        'Россия, Башкортостан респ.': 41,
        'Россия, Бурятия респ.': 10,
        'Россия, Алтай респ.': 2,
        'Россия, Дагестан респ.': 26,
        'Россия, Ингушетия респ.': 5,
        'Россия, Кабардино-Балкарская респ.': 9,
        'Россия, Калмыкия - Хальмг Тангч респ.': 3,
        'Россия, Карачаево-Черкесская респ.': 4,
        'Россия, Карелия респ.': 7,
        'Россия, Коми респ.': 10,
        'Россия, Марий Эл респ.': 7,
        'Россия, Мордовия респ.': 9,
        'Россия, Саха (Якутия) респ.': 9,
        'Россия, Северная Осетия респ.': 7,  # Алания
        'Россия, Татарстан респ.': 38,
        'Россия, Тыва (Тува) респ.': 3,
        'Россия, Удмуртская респ.': 15,
        'Россия, Хакасия респ.': 5,
        'Россия, Чеченская респ.': 12,
        'Россия, Чувашская респ.': 13,
        'Россия, Алтайский край': 25,
        'Россия, Краснодарский край': 51,  # Кубань
        'Россия, Красноярский край': 30,  # TODO: taymir, evenikii???
        'Россия, Приморский край': 20,
        'Россия, Ставропольский край': 27,
        'Россия, Хабаровский край': 14,
        'Россия, Амурская обл.': 9,
        'Россия, Архангельская обл.': 13,
        'Россия, Астраханская обл.': 10,
        'Россия, Белгородская обл.': 15,
        'Россия, Брянская обл.': 13,
        'Россия, Владимирская обл.': 15,
        'Россия, Волгоградская обл.': 26,
        'Россия, Вологодская обл.': 12,
        'Россия, Воронежская обл.': 23,
        'Россия, Ивановская обл.': 11,
        'Россия, Иркутская обл.': 27,  # Ust-ordinskii???
        'Россия, Калининградская обл.': 9,
        'Россия, Калужская обл.': 10,
        'Россия, Камчатский край': 3,  # Koryakskii???
        'Россия, Кемеровская обл.': 28,
        'Россия, Кировская обл.': 14,  # Вятка
        'Россия, Костромская обл.': 7,
        'Россия, Курганская обл.': 10,
        'Россия, Курская обл.': 12,
        'Россия, Ленинградская обл.': 62,
        'Россия, Липецкая обл.': 12,
        'Россия, Магаданская обл.': 2,
        'Россия, Московская обл.': 171,
        'Россия, Мурманская обл.': 9,
        'Россия, Нижегородская обл.': 34,
        'Россия, Новгородская обл.': 7,
        'Россия, Новосибирская обл.': 26,
        'Россия, Омская обл.': 20,
        'Россия, Оренбургская обл.': 21,
        'Россия, Орловская обл.': 8,
        'Россия, Пензенская обл.': 14,
        'Россия, Пермский край': 27,  # Komi-permyatskii???
        'Россия, Псковская обл.': 7,
        'Россия, Ростовская обл.': 43,
        'Россия, Рязанская обл.': 12,
        'Россия, Самарская обл.': 32,
        'Россия, Саратовская обл.': 26,
        'Россия, Сахалинская обл.': 5,
        'Россия, Свердловская обл.': 44,
        'Россия, Смоленская обл.': 10,
        'Россия, Тамбовская обл.': 11,
        'Россия, Тверская обл.': 14,
        'Россия, Томская обл.': 10,
        'Россия, Тульская обл.': 16,
        'Россия, Тюменская обл.': 33,
        'Россия, Ульяновская обл.': 13,
        'Россия, Челябинская обл.': 35,
        'Россия, Забайкальский край': 12,  # angiro-buryatskii???
        'Россия, Ярославская обл.': 13,
        'Россия, Еврейская авт. обл.': 2,
        'Россия, Крым Авт. Респ.': 25,
        'Россия, Чукотский авт. окр.': 2,
    }

    result_table = {}
    for region in number_of_caches_to_get_diploma:
        if region in regions_to_caches_table:
            result_table[region] = {}
            result_table[region]['neightbors'] = []
            found_in_the_region = len(regions_to_caches_table[region])
            caches_here = min(number_of_caches_to_get_diploma[region], found_in_the_region)
            caches_to_display = regions_to_caches_table[region][:caches_here]

            score = caches_here
            max_score = number_of_caches_to_get_diploma[region] + len(get_region_neighbours(region))

            for neightbour in get_region_neighbours(region):
                value_to_add = (neightbour, None)
                if neightbour in regions_to_caches_table and regions_to_caches_table[neightbour]:
                    value_to_add = (neightbour, regions_to_caches_table[neightbour][0])
                    score += 1
                result_table[region]['neightbors'].append(value_to_add)

            result_table[region]['caches'] = caches_to_display
            result_table[region]['total_score'] = score
            result_table[region]['region_score'] = caches_here
            result_table[region]['region_max_score'] = number_of_caches_to_get_diploma[region]
            result_table[region]['max_score'] = max_score
            result_table[region]['can_get'] = max_score == score

    a = 2
    return result_table


if __name__ == '__main__':
    qqq = check_regions_for_user(4786)
    print(qqq)
    pass
