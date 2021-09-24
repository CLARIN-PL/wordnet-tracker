

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
        '5': 'bhp',
        '7': 'czy',
        '9': 'wytw',
        '11': 'cech',
        '13': 'czc',
        '15': 'umy',
        '17': 'por',
        '19': 'zdarz',
        '21': 'czuj',
        '23': 'jedz',
        '25': 'grp',
        '27': 'msc',
        '29': 'cel',
        '31': 'rz',
        '33': 'os',
        '35': 'zj',
        '37': 'rsl',
        '39': 'pos',
        '41': 'prc',
        '43': 'il',
        '45': 'zw',
        '47': 'ksz',
        '49': 'st',
        '51': 'sbst',
        '53': 'czas',
        '55': 'zwz',
        '57': 'hig',
        '59': 'zmn',
        '61': 'cumy',
        '63': 'cpor',
        '65': 'wal',
        '67': 'cjedz',
        '69': 'dtk',
        '71': 'cwyt',
        '73': 'cczuj',
        '75': 'ruch',
        '77': 'pst',
        '79': 'cpos',
        '81': 'sp',
        '83': 'cst',
        '85': 'pog',
        '87': 'jak',
        '89': 'rel',
        '91': 'odcz',
        '101': 'sys',
        '93': 'adj',
        '95': 'adv',
        '97': 'mat',
        '99': 'grad',
        '103': 'cdystr',
        '105': 'caku',
        '107': 'cper',
        '109': 'cdel'
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
