""" Helper functions """


def addToAverage(totalCount, totalValue, newValue):
    """ simple sliding average calculation """
    return ((1.0 * totalCount * totalValue) + newValue) / (totalCount + 1)
