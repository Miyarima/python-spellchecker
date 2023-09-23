#!/usr/bin/env python3
#pylint: disable=protected-access
""" Module for testing the trie class """

import unittest
from src.trie import Trie
from src.node import Node
from src.errors import SearchMiss

class TestSpellcheker(unittest.TestCase):
    """
    Class for testing the trie class
    """

    def test_adding_a_word(self):
        """ Adding a word """
        trie = Trie()
        trie.add_word("hello")
        self.assertIsInstance(trie.check_if_exists("hello"), Node)

    def test_remove(self):
        """ Removing a word """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        trie.remove("markus")
        with self.assertRaises(SearchMiss) as _:
            trie.check_if_exists("markus")

    def test_remove_that_doesnt_exist(self):
        """ Removing a word that doesn't exist """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        with self.assertRaises(SearchMiss) as _:
            trie.remove("kalle")

    def test_all_words(self):
        """ Retrieving all words """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("hella")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        self.assertEqual(trie.all_words(), ["hello", "hella", "help", "markus", "marcus"])

    def test_word_count(self):
        """ Words count """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("hella")
        trie.add_word("help")
        trie.add_word("helpless")
        trie.add_word("markus")
        trie.add_word("marcus")
        self.assertEqual(trie.word_count(), 6)

    def test_prefix_search(self):
        """ Prefix search """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        self.assertEqual(trie.prefix_search("ma"), [('markus', 1.0), ('marcus', 1.0)])

    def test_prefix_search_empty(self):
        """ Prefix search empty result """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        self.assertEqual(trie.prefix_search("op"), [])

    def test_suffix_search(self):
        """ Suffix search empty result """
        trie = Trie()
        trie.add_word("hello")
        trie.add_word("help")
        trie.add_word("markus")
        trie.add_word("marcus")
        self.assertEqual(trie.suffix_search("op"), [])
