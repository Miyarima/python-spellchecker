"""
This is a module containing the Errors class
"""

class Error(Exception):
    """User defined class for custom exceptions"""

class SearchMiss(Error):
    """ This word does not exist"""
