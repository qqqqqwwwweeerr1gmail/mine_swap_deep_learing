import json


def init_file(path,title):
    d = {
        title: {}
    }
    with open(path, 'w') as f:
        json.dump(d, f)


def init_value(plob):
    # select value
    plob_ima = [[y + str(1) if y.startswith('?') else y for y in x] for x in plob]
    return plob_ima


if __name__ == '__main__':
    memo_path = 'memo.json'
    suspect_path = 'suspect.json'
    knowledge_path = 'knowledge.json'
    edr_path = 'edr.json'
    edr_value_path = 'edr_value.json'

    # init_memo(memo_path)
    # init_knowledge(knowledge_path)
    # init_suspect(suspect_path)
    # init_edr(edr_path)
    # init_edr_value(edr_value_path)

    init_file(memo_path, title='memo')
    init_file(knowledge_path, title='knowledge')
    init_file(suspect_path, title='suspect')
    init_file(edr_path, title='edr')
    init_file(edr_value_path, title='edr_value')


