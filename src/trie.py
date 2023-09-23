"""
This is a module containing the Trie class
"""
from src.node import Node
from src.errors import SearchMiss

class Trie:
    """ The Trie class """
    def __init__(self, words=None, frequency=None):
        self.root = Node("", False)
        self._total_words = 0
        if words is not None:
            if frequency is not None:
                for i, word in enumerate(words):
                    self.add_word(word, frequency[i])
            else:
                for w in words:
                    self.add_word(w)

    def add_word(self, word, frequency=1):
        """ Add chars into the Trie """
        word = word.lower()
        if word[0] not in self.root.children:
            self.root.children[word[0]] = Node(word[0], False)
        self._add_word(self.root, word, frequency)
        self._total_words += 1

    @classmethod
    def _add_word(cls, node, word, frequency):
        if len(word) == 0:
            node.stop = True
            node.frequency = frequency
            return
        if word[0] in node.children:
            cls._add_word(node.children[word[0]], word[1:], frequency)
        elif not word[0] in node.children:
            if cls._end_of_word(word):
                node.children[word[0]] = Node(word[0], cls._end_of_word(word), node, frequency)
            else:
                node.children[word[0]] = Node(word[0], cls._end_of_word(word), node)
            if len(word) > 1:
                cls._add_word(node.children[word[0]], word[1:], frequency)

    @staticmethod
    def _end_of_word(word):
        return len(word) == 1

    def check_if_exists(self, word):
        """ Checks if the given word exists """
        word = word.lower()
        if word[0] not in self.root.children:
            raise SearchMiss
        return self._check_if_exists(self.root, word)

    @classmethod
    def _check_if_exists(cls, node, word):
        try:
            if node.stop and len(word) == 0:
                return node
            if word[0] in node.children:
                return cls._check_if_exists(node.children[word[0]], word[1:])
            raise SearchMiss
        except IndexError as exc:
            raise SearchMiss from exc

    def remove(self, word):
        """ Checks if the given word exists """
        word = word.lower()
        node = self.check_if_exists(word)
        self._total_words -= 1
        return self._remove(node, word)

    @classmethod
    def _remove(cls, node, word):
        if node.has_no_children():
            node.parent.children.pop(node.value)
            return cls._remove(node.parent, word)
        if node.has_children() and node.value == word[-1]:
            node.stop = False
        return None

    def word_count(self):
        """ Returns the number of words """
        return self._total_words

    def all_words(self):
        """ Returns all words in the trie """
        return self._all_words(self.root, "", [])

    @classmethod
    def _all_words(cls, node, word_str, words):
        word_str += node.value
        if node.stop:
            words.append(word_str)
        for value in node.children.values():
            words = cls._all_words(value, word_str, words)
        return words

    def prefix_search(self, pre):
        """ Returns all words with the right prefix """
        res = []
        pre = pre.lower()
        found_words = self._prefix_search(self.root, "", [], pre)
        found_words = sorted(found_words, key=lambda x: float(x[1]), reverse=True)
        found_words = found_words[:10]
        for word in found_words:
            res.append((word[0], float(word[1])))
        return res

    @classmethod
    def _prefix_search(cls, node, word_str, words, pre):
        word_str += node.value
        if node.stop and cls._prefix_compare(pre, word_str):
            words.append([word_str, node.frequency])
        for value in node.children.values():
            words = cls._prefix_search(value, word_str, words, pre)
        return words

    @staticmethod
    def _prefix_compare(pre, word_str):
        if pre == word_str[:len(pre)]:
            return True
        return False

    def suffix_search(self, suf):
        """ Returns all words with the right prefix """
        suf = suf.lower()
        found_words = self._sufffix_search(self.root, "", [], suf)
        found_words = sorted(found_words)
        return found_words

    @classmethod
    def _sufffix_search(cls, node, word_str, words, suf):
        word_str += node.value
        if node.stop and cls._suffix_compare(suf, word_str):
            words.append(word_str)
        for value in node.children.values():
            words = cls._sufffix_search(value, word_str, words, suf)
        return words

    @staticmethod
    def _suffix_compare(suf, word_str):
        if suf == word_str[-len(suf):]:
            return True
        return False

    def correct_spelling(self, sugg):
        """ Returns all words with similar spelling """
        sugg = sugg.lower()
        found_words = self._suggestions(self.root, "", [], sugg)
        found_words = sorted(found_words)
        if sugg in found_words:
            return [sugg]
        return found_words

    @classmethod
    def _suggestions(cls, node, word_str, words, sugg):
        word_str += node.value
        if node.stop and cls._suggestions_compare(sugg, word_str):
            words.append(word_str)
        for value in node.children.values():
            words = cls._suggestions(value, word_str, words, sugg)
        return words

    @staticmethod
    def _suggestions_compare(sugg, word_str):
        if len(sugg) == len(word_str) and sugg[-1] == word_str[-1]:
            wrong_counter = 0
            for i, letter in enumerate(sugg):
                if letter != word_str[i]:
                    wrong_counter += 1
                elif letter == word_str[i] and wrong_counter < 2:
                    wrong_counter = 0
            if wrong_counter < 2:
                return True
        return False

    @classmethod
    def create_from_file(cls, filename="frequency.txt"):
        """ Loads the words from a file """
        with open(filename, "r", encoding="utf8") as f:
            file_contents = [line.rstrip() for line in f]
        if "frequency" in filename:
            words = []
            frequency = []
            for line in file_contents:
                line = line.split(" ")
                words.append(line[0])
                frequency.append(line[1])
            return cls(words, frequency)
        return cls(file_contents)
