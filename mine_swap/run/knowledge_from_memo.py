




import time
from mine_swap.tools.record_memo import read_memo
from mine_swap.tools.bayes_ana import content_diff_sorted
from mine_swap.tools.generate_info_EDR import content2EDR
from mine_swap.tools.load_info import get_all_last_plob
from mine_swap.tools.generate_knowledge import write_up_edr,correct_edr2knowledge

from mine_swap.tools.init_func import init_value,init_file

if __name__ == '__main__':
    memo_path = 'memo.json'
    edr_value_path = 'edr_value.json'
    knowledge_path = 'knowledge.json'
    edr_path = 'edr.json'
    read_memo_num = 500
    knowledge_no = int(time.time() * 1_000_000)

    is_ana_init = False
    is_ana_init = True

    if is_ana_init:
        # init_file(memo_path, title='memo')
        init_file(knowledge_path, title='knowledge')
        init_file(edr_path, title='edr')
        init_file(edr_value_path, title='edr_value')

    all_last_plob = get_all_last_plob(memo_path)

    focus_content = read_memo(memo_path, read_memo_num)

    sorted_fo_content = content_diff_sorted(focus_content, bayes_epoch=100)

    for con in sorted_fo_content:
        print(con)
        EDRs = content2EDR(con)
        for EDR in EDRs:
            write_up_edr(EDR,all_last_plob,edr_path=edr_path,edr_value_path=edr_value_path,knowledge_path=knowledge_path)

    correct_edr2knowledge(knowledge_no,edr_value_path=edr_value_path,knowledge_path=knowledge_path)

















