



if __name__ == '__main__':
    col_num = 2
    row_num = 3
    total_reward = 0
    success_reward = 0
    failure_reward = -1
    memo_path = 'memo.json'
    suspect_path = 'suspect.json'
    knowledge_path = 'knowledge.json'
    edr_path = 'edr.json'
    edr_value_path = 'edr_value.json'

    read_theme_num = 50

    # is rerun flag
    is_escape_memo = True
    is_escape_memo = False
    memo_episode = 100

    if is_escape_memo:
        memo_episode = 0


    for i in range(memo_episode):
        # print('=-----------------'+str(i)+'  episode=-----------------')
        env = new_env()
        raw_env = list(map(list, zip(*env)))
        actual_env = show_and_count(raw_env, re=True, name='raw_env')
        env_time_stamp = int(time.time() * 1_000_000)

        plob = init_player_ob()
        #  print(plob)
        #  print(actual_env)
        #  show(plob,  name='plob'
        #  print(actual_env)
        #  raw_show(plob, name='plob')

        sim_till_end(plob, record_flag=True)
    print(total_reward)
    try:
        rate_reward = total_reward / memo_episode
        print(rate_reward)
    except:
        pass















