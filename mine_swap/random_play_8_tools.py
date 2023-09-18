from mine_swap.tools.create_env import new_env,actual_env_4_raw,print_env,init_player_ob





if __name__ == '__main__':
    row_num = 3
    col_num = 3
    env = new_env(row_num,col_num)
    print('init_env: ',env)
    raw_env = list(map(list, zip(*env)))
    print('init_env_row_ranked: ', raw_env)  # 0 represent a mine and 1 represent not mine
    actual_env = actual_env_4_raw(raw_env)
    print_env(actual_env, name='actual_env')
    # actual_env = show_and_count(raw_env, re=True, name='actual_env')
    # print(actual_env)
    plob = init_player_ob(actual_env)
    print_env(plob, name='plob')
    # print(plob)




















