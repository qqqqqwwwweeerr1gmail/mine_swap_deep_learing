import json

memo_path = 'memo.json'

with open(memo_path) as f:
    d = json.load(f)
    records = len(d['record'])
    print(records)

    max_length = 0
    for record_no in range(records):
        content = d['record'][record_no]['content']
        # print(content)
        len_content = len(content)
        print(len_content)
        if len_content>max_length:
            max_length = len_content
    print(max_length)












