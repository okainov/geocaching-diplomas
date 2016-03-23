# -*- coding: utf-8 -*-

cache_types_lookup = {'Традиционный': 'TR',
                      'Виртуальный': 'VI',
                      'Пошаговый традиционный': 'MS',
                      'Пошаговый виртуальный': 'MV'}


class Cache:

    def __init__(self, xml_data):
        self.cache_type = cache_types_lookup[xml_data.findall('type')[0].text]
        self.cache_id = xml_data.findall('id')[0].text
        self.name = xml_data.findall('name')[0].text

    def __init__(self, id, type, name, author, creation_date, region):
        self.cache_type = type.upper()
        self.cache_id = id
        self.name = name
        self.author = author
        self.region = region
        self.creation_date = creation_date

    def __repr__(self):
        return '%s/%s: %s' % (self.cache_type, self.cache_id, self.name)

    def get_link(self):
        return 'http://www.geocaching.su/?pn=101&cid=%s' % self.cache_id
