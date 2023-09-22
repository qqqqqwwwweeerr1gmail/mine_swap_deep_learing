import json,random
import math

def get_last_knowledge_no(knowledge_path='knowledge.json'):
    with open(knowledge_path) as f:
        d = json.load(f)
    return list(d['knowledge'].keys())[-1]


def get_all_last_plob(memo_path='memo.json'):
    with open(memo_path) as f:
        d = json.load(f)
    all_last_plob = [x['content'][-1]['plob'] for x in d['record']]
    return all_last_plob


def read_memo(memo_path, num, va_down=-math.inf, va_up=0):
    focus_plob = []

    with open(memo_path) as f:
        d = json.load(f)

    for record in d['record']:
        for content in record['content']:
            if va_down < content['beneficial'] < va_up:
                focus_plob.append(content)
    """random select from record"""
    focus_content = random.sample(focus_plob, num)
    return focus_content


def filter_succ_plob(ls_plob):
    ls_succ_plob = []
    ls_fail_plob = []
    for plob in ls_plob:
        succ = True
        for col in plob:
            if '*' in col:
                succ = False
        if succ:
            ls_succ_plob.append(plob)
        else:
            ls_fail_plob.append(plob)
    return ls_succ_plob,ls_fail_plob



if __name__ == '__main__':
    memo_path = 'memo.json'
    suspect_path = 'suspect.json'
    knowledge_path = 'knowledge.json'
    read_theme_num = 50

    last_knowledge_no = get_last_knowledge_no(knowledge_path)
    print(last_knowledge_no)
    all_last_plob = get_all_last_plob(memo_path)
    print(all_last_plob)
    ls_succ_plob,ls_fail_plob = filter_succ_plob(all_last_plob)
    print(ls_succ_plob)
    print(ls_fail_plob)

    focus_content = read_memo(memo_path, read_theme_num)
    print(focus_content)








