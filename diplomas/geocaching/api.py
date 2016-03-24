# -*- coding: utf-8 -*-
import re

import urllib.request
import xml.etree.ElementTree
from diplomas.geocaching.cache import Cache


def get_page_by_url(url):
    r = urllib.request.urlopen(url)
    bytes_str = r.read()
    return bytes_str.decode('cp1251')

def get_page_by_url_without_encoding(url):
    return urllib.request.urlopen(url).read()

def get_cache_details(cache_id):
    page_src = get_page_by_url_without_encoding('http://www.geocaching.su/site/api.php?rtype=2&cid=%s&istr=ems' % cache_id)
    root = xml.etree.ElementTree.fromstring(page_src)
    return Cache.init_from_xml(root)


def get_user_finds(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=2&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src)


def get_user_creations(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=1&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src)


def get_user_nickname(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=2&uid=%s" % user_id)
    return extract_nickname_from_webpage(page_src)


def extract_nickname_from_webpage(page_src):
    cache_re = re.compile('<h1 class=hdr>(.+?)</h1>', flags=re.DOTALL | re.UNICODE)
    try:
        return cache_re.findall(page_src)[0]
    except:
        return None


def extract_caches_from_webpage(page_src):
    re_for_created_cache = re.compile('alt=.(?P<type>\w\w).*?<a href=.*?pn=101&cid=(?P<id>\d+).*?blank>(?P<name>.*?)</a>.*?(?P<cdate>\d\d.\d\d.\d\d\d\d), (?P<region>.*?)[\(\d<]', flags=re.DOTALL | re.UNICODE)
    re_for_found_cache = re.compile('<tr><td>.*?/ctypes/icons/.*?alt=.(?P<type>\w\w).*?<a href=.*?pn=101&cid=(?P<id>\d+).*?blank>(?P<name>.*?)</a>.*?<b>(?P<creator>.*?)</b>.*?\((?P<cdate>\d\d.\d\d.\d\d\d\d), (?P<region>.*?)\)', flags=re.DOTALL | re.UNICODE)
    if 'Созданные тайники' in page_src:
        cache_re = re_for_created_cache
    else:
        cache_re = re_for_found_cache

    caches = list()
    n_all_finds = len(cache_re.findall(page_src))
    for i, re_match in enumerate(cache_re.finditer(page_src)):

        cache_id = re_match.group('id')
        cache_type = re_match.group('type')
        try:
            cache_creator = re_match.group('creator')
        except IndexError:
            cache_creator = extract_nickname_from_webpage(page_src)
        cache_name = re_match.group('name')
        creation_date = re_match.group('cdate')
        region = re_match.group('region')
        if 'рейтинг' in region:
            region = region[:-10]
        region = region.strip()
        if region == 'Россия, Тыва (Тува':
            region = 'Россия, Тыва (Тува) респ.'
        elif 'Саха' in region and 'Сахалин' not in region:
            region = 'Россия, Саха (Якутия) респ.'

        if i % 100 == 0:
            print('%s\\%s' % (i, n_all_finds))
        current_cache = Cache.init_from_fields(cache_id, cache_type, cache_name, cache_creator, creation_date, region)
        caches.append(current_cache)
    return caches