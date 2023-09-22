







if __name__ == '__main__':
    from mine_swap.tools.record_memo import play_batch
    from mine_swap.tools.load_info import get_last_knowledge_no

    if __name__ == '__main__':
        row_num = 3
        col_num = 2
        episode = 1000
        knowledge_no = knowledge_time = get_last_knowledge_no()

        # total_reward = random_play_batch(row_num, col_num, init_reward=0, episode=1000)
        batch_reward = play_batch(row_num, col_num, init_reward=0, episode=episode, record_flag=False,conjecture=True,
                                  memo_path='memo.json',knowledge_no=knowledge_no)
        print(batch_reward)
        print('knowledge play win rate', batch_reward / episode)

        import json

        memo_path = 'memo.json'

        with open(memo_path) as f:
            d = json.load(f)
            length = len(d['record'])
        print(length)
















