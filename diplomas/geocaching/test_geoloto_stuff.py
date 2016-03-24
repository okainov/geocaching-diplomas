# -*- coding: utf-8 -*-

from unittest import TestCase

from diplomas.geocaching.geoloto_stuff import get_cache_to_number_table_with_simple_singleton_two, \
    get_cache_to_number_table_with_two_equal_pairs


class TestGet_cache_to_number_table_with_simple_singleton_two(TestCase):
    def test_list_with_two_caches(self):
        result = {}
        get_cache_to_number_table_with_simple_singleton_two('T', {'TR010': ['0', '1']}, result)
        self.assertEqual(result, {'0': {'T': 'TR010'}})

    def test_two_lists_with_two_caches_equal(self):
        result = {}
        get_cache_to_number_table_with_simple_singleton_two('T', {'TR010': ['0', '1'], 'TR100': ['0', '1']}, result)
        self.assertEqual(result, {})

    def test_two_lists_with_two_caches_nequal(self):
        result = {}
        get_cache_to_number_table_with_simple_singleton_two('T', {'TR010': ['0', '1'], 'TR23': ['2', '3']}, result)
        self.assertEqual(result, {'0': {'T': 'TR010'},
                                  '2': {'T': 'TR23'}})


class TestGet_cache_to_number_table_with_two_equal_pairs(TestCase):
    def test_two_lists_with_two_caches_equal(self):
        result = {}
        get_cache_to_number_table_with_two_equal_pairs('T', {'TR010': ['0', '1'], 'TR100': ['0', '1']}, result)
        self.assertEqual(result, {'0': {'T': 'TR010'},
                                  '1': {'T': 'TR100'}})
