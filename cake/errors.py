class MissingValue(Exception):
    """ Raised when no value was specified for a var """

class InvalidObject(Exception):
    """ Raised when the object provided doesn't have a specific attribute/method """

class EquationParseError(Exception):
    """ Raised when an error occurs whilst parsing your equation """

class SubstitutionError(Exception):
    """ Raised when an error occurs during substitution """
