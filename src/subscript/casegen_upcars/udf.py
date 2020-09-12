""" Supporting functions/class for casegen_upcars """
import numpy as np
from scipy.stats import uniform

TERMINALCOLORS = {
    "HEADER": "\033[95m",
    "OKBLUE": "\033[94m",
    "OKGREEN": "\033[92m",
    "WARNING": "\033[93m",
    "FAIL": "\033[91m",
    "ENDC": "\033[0m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}


def iter_flatten(iterable):
    """
    Flatten multi-dimension iterable
    """
    it_obj = iter(iterable)
    for enum_obj in it_obj:
        if isinstance(enum_obj, (list, tuple)):
            for flatten_obj in iter_flatten(enum_obj):
                yield flatten_obj
        else:
            yield enum_obj


def flatten(list_obj):
    """
    Flatten multi-dimension iterable, ensure returning value is a list
    """
    return list(iter_flatten(list_obj))  # [i for i in iter_flatten(list_obj)]


def listify(source, count, conversion_func=None):
    """
    Return list of source with length of count if source is not already a list
    """
    if isinstance(source, list):
        # Adjust the size when it is only 1 item
        if len(source) == 1:
            source = source * count

        if conversion_func is None:
            return source
        return [conversion_func(i) for i in source]

    if conversion_func is None:
        return [source] * count
    return [conversion_func(source)] * count


def uniform_dist(low, high, size, seed_nr=None):
    """
    Generate uniform distribution which range from low - high
    """
    if low == high:
        return np.full(size, low)
    if seed_nr is not None:
        np.random.seed(seed_nr)
    return uniform.rvs(low, high - low, size=size)


def compact_list(data):
    """
    Generate a compact representation of list value
    Useful in Eclipse context to make smaller file size and faster file writing
    For example::

      compact_list([1 1 1 1 2 1 1 1]) -> 4*1 2 3*1

    """
    list_value = [data[0]]
    list_count = [1]
    for idx in range(1, len(data)):
        if data[idx] == list_value[-1]:
            list_count[-1] += 1
        else:
            list_value.append(data[idx])
            list_count.append(1)
    str_ = ""
    for idx, value in enumerate(list_value):
        str_ += (
            " {}*{}".format(list_count[idx], value)
            if list_count[idx] > 1
            else " {}".format(value)
        )
    return str_


def conversion(variable, conversion_func=float):
    """
    Convert value/list to anything using conversion function
    :param variable: any value/list to convert
    :return: converted value/list of value
    """
    if isinstance(variable, list):
        return [conversion_func(x) for x in variable]
    return conversion_func(variable)
