def value_present(value, dictionary) -> bool:
    assert isinstance(dictionary, dict)
    return any([
        True for val in dictionary.values()
        if str(value) in str(val)
    ])


def sort_by_attr(lst, attribute, order_arg):
    def _get_attr(obj):
        if hasattr(obj, attribute):
            attr = getattr(obj, attribute)
            if attr is not None:
                return attr
            else:
                return '~'
        else:
            return obj

    assert isinstance(lst, list)
    if order_arg == 'asc':
        _reverse = False
    else:
        _reverse = True
    lst.sort(key=lambda x: _get_attr(x), reverse=_reverse)
