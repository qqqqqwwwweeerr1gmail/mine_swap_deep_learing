import json, random

def read_edr(edr_path):
    with open(edr_path) as f:
        d_edr = json.load(f)['edr']
    return d_edr


def read_knowledge(knowledge_path):
    with open(knowledge_path) as f:
        d_knowledge = json.load(f)['knowledge']
    return d_knowledge

def read_edr_value():
    global edr_value_path
    with open(edr_value_path) as f:
        d_edr_value = json.load(f)['edr_value']
    return d_edr_value


# def read_theme(memo_path, num):
#     focus_plob = []
#     with open(memo_path) as f:
#         d = json.load(f)
#     for record in d['record']:
#         for content in record['content']:
#             if content['beneficial'] < 0:
#                 focus_plob.append(content['plob'])
#     focus_plob = [focus_plob[int(random.random() * len(focus_plob))] for x in range(num)]
#     return focus_plob


def read_theme(memo_path, num):
    focus_plob = []

    with open(memo_path) as f:
        d = json.load(f)

    for record in d['record']:
        for content in record['content']:
            if content['beneficial'] < 0:
                focus_plob.append(content)
    focus_content = [focus_plob[int(random.random() * len(focus_plob))] for x in range(num)]
    return focus_content













