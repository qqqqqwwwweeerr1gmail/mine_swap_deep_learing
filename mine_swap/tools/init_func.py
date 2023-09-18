import json

def init_json(path,title):
    d = {
        title: {}
    }
    with open(path, 'w') as f:
        json.dump(d, f)

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

    init_json(memo_path, title='memo')
    init_json(knowledge_path, title='knowledge')
    init_json(suspect_path, title='suspect')
    init_json(edr_path, title='edr')
    init_json(edr_value_path, title='edr_value')