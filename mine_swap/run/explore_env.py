






from mine_swap.tools.record_memo import play_batch



if __name__ == '__main__':
    row_num = 2
    col_num = 3
    episode = 1
    # total_reward = random_play_batch(row_num, col_num, init_reward=0, episode=1000)
    total_reward = play_batch(row_num, col_num, init_reward=0, episode=episode,record_flag=True,memo_path='memo.json')
    print(total_reward)
    print('random play win rate', total_reward / episode)

    import json

    memo_path = 'memo.json'

    with open(memo_path) as f:
        d = json.load(f)
        length = len(d['record'])
    print(length)










