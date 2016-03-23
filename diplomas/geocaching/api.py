# -*- coding: utf-8 -*-

import urllib.request
import xml
from diplomas.geocaching.cache import Cache
from diplomas.geocaching.utils import extract_nickname_from_webpage, extract_caches_from_webpage


def get_page_by_url(url):
    r = urllib.request.urlopen(url)
    bytes_str = r.read()
    return bytes_str.decode('cp1251')


def get_cache_details(cache_id):
    page_src = get_page_by_url('http://www.geocaching.su/site/api.php?rtype=2&cid=%s&istr=ems' % cache_id).read()
    root = xml.etree.ElementTree.fromstring(page_src)
    return Cache(root)


def get_user_finds(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=2&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src)


def get_user_creations(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=1&uid=%s" % user_id)
    return extract_caches_from_webpage(page_src)


def get_user_nickname(user_id):
    page_src = get_page_by_url("http://www.geocaching.su/site/popup/userstat.php?s=2&uid=%s" % user_id)
    return extract_nickname_from_webpage(page_src)