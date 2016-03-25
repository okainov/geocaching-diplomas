# -*- coding: utf-8 -*-

cache_types_lookup = {'Традиционный': 'TR',
                      'Виртуальный': 'VI',
                      'Пошаговый традиционный': 'MS',
                      'Пошаговый виртуальный': 'MV'}


class Cache:

    cache_type = None
    cache_id = None
    name = None
    author = None
    region = None
    creation_date = None
    find_date = None

    @classmethod
    def init_from_xml(cls, xml_data):
        cache = Cache()
        cache.cache_type = cache_types_lookup[xml_data.findall('type')[0].text]
        cache.cache_id = xml_data.findall('id')[0].text
        cache.name = xml_data.findall('name')[0].text
        cache.creation_date = xml_data.findall('date')[0].text
        return cache

    def __repr__(self):
        return '%s/%s: %s (%s, %s)' % (self.cache_type, self.cache_id, self.name, self.creation_date, self.find_date)

    def short_repr(self):
        return '%s/%s' % (self.cache_type, self.cache_id)

    def get_repr_id_and_name(self):
        return '%s/%s: %s' % (self.cache_type, self.cache_id, self.name)

    def get_link(self):
        return 'http://www.geocaching.su/?pn=101&cid=%s' % self.cache_id
