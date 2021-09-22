

def parts_of_speech():
    return {
        'None': '',
        '1': 'Verb',
        '2': 'Noun',
        '3': 'Adverb',
        '4': 'Adjective',
        '5': 'Verb Princeton',
        '6': 'Noun Princeton',
        '7': 'Adverb Princeton',
        '8': 'Adjective Princeton'
    }


def status():
    return {
        'None': {'value': '', 'tag': ''},
        '122': {'value': 'Unprocessed', 'tag': 'label-default'},
        '123': {'value': 'New', 'tag': 'label-primary'},
        '124': {'value': 'Error', 'tag': 'label-danger'},
        '125': {'value': 'Checked', 'tag': 'label-success'},
        '126': {'value': 'Meaning', 'tag': 'label-info'},
        '127': {'value': 'Partially Checked', 'tag': 'label-warning'}
}


def domain():
    return {
        'None': '',
        '1': 'bhp',
        '2': 'czy',
        '3': 'wytw',
        '4': 'cech',
        '5': 'czc',
        '6': 'umy',
        '7': 'por',
        '8': 'zdarz',
        '9': 'czuj',
        '10': 'jedz',
        '11': 'grp',
        '12': 'msc',
        '13': 'cel',
        '14': 'rz',
        '15': 'os',
        '16': 'zj',
        '17': 'rsl',
        '18': 'pos',
        '19': 'prc',
        '20': 'il',
        '21': 'zw',
        '22': 'ksz',
        '23': 'st',
        '24': 'sbst',
        '25': 'czas',
        '26': 'zwz',
        '27': 'hig',
        '28': 'zmn',
        '29': 'cumy',
        '30': 'cpor',
        '31': 'wal',
        '32': 'cjedz',
        '33': 'dtk',
        '34': 'cwyt',
        '35': 'cczuj',
        '36': 'ruch',
        '37': 'pst',
        '38': 'cpos',
        '39': 'sp',
        '40': 'cst',
        '41': 'pog',
        '42': 'jak',
        '43': 'rel',
        '44': 'odcz',
        '46': 'sys',
        '47': 'adj',
        '48': 'adv',
        '49': 'mat',
        '45': 'grad',
        '50': 'cdystr',
        '51': 'caku',
        '52': 'cper',
        '53': 'cdel'
    }


def aspect():
    return {
        'None': '',
        '0': 'Not a verb',
        '1': 'Perfective',
        '2': 'Imperfective',
        '3': 'Predicative',
        '4': 'Two aspect verb'
    }
