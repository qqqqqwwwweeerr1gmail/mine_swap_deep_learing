import json


def frush_obj(file_name):
    """ 清空记忆 """
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write('')
        f.close()


def get_n_s():
    """ get suspect """
    with open('suspect.json') as f:
        d = json.load(f)
    try:
        return max([int(x) for x in list(d['suspect'].keys())])
    except:
        return ''


def get_n_k():
    """ get knowledge """
    with open('knowledge.json') as f:
        d = json.load(f)
    try:
        return max([int(x) for x in list(d['knowledge'].keys())])
    except:
        return ''
























