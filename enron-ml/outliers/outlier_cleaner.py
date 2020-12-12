#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """
    import numpy

    cleaned_data = []

    error = (predictions - net_worths)**2
    for i in range(9):
        max_index = error.argmax()
        ages = numpy.delete(ages, max_index)
        net_worths = numpy.delete(net_worths, max_index)
        error = numpy.delete(error, max_index)

    cleaned_data = [(ages[i],net_worths[i],e) for i,e in enumerate(error)]

    return cleaned_data
