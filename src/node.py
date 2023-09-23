"""
This is a module containing the node class
"""

class Node:
    """ The Node class """
    def __init__(self, value, stop, parent=None, frequency=None):
        self.value = value
        self.stop = stop
        self.frequency = frequency
        self.parent = parent
        self.children = {}

    def has_no_children(self):
        """ Returns False if the left child is none """
        return not self.children

    def has_children(self):
        """ Returns False if the left child is none """
        return self.children

    def is_word(self):
        """ Returns False if the right child is none """
        return self.stop

    def __contains__(self, other):
        return other in self.children
