class MissingValue(Exception):
    """ Raised when no value was specified for a var """

class InvalidObject(Exception):
    """ Exception raised when the objest provided doesn't have a specific attribute/method """

class EquationParseError(Exception):
    """ Raised when an error occurs whilst parsing your equation equation """
