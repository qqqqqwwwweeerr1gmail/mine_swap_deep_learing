
all_last_plob = get_all_last_plob()

focus_content = read_theme(memo_path, read_theme_num)

diff_content_ls = []
for fc in focus_content:
    print(fc)
    fo = fc['plob']
    print(fo)
    print(fc['action'])
    # [[' 1 ', '?'], [' 1 ', '?'], ['*', '?']]
    # (2, 0)
    bf_fo = bffo(fo, fc['action'])
    print(bf_fo)
    # [[' 1 ', '?'], [' 1 ', '?'], ['?', '?']]
    plob_ima = init_value(bf_fo)
    print(plob_ima)
    # [[' 1 ', '?0.1'], [' 1 ', '?0.1'], ['?0.1', '?0.1']]
    re_bayes_ima = bayes_mine_value(fo, 1000)
    print(re_bayes_ima)
    # [[' 1 ', ' 1 ', '*'], ['$*****','$1111111','$1111']]
    re_bayes_rate = bayes_mine_rate(re_bayes_ima)
    print(re_bayes_rate)
    # [[' 1 ', ' 1 ', '*'], ['@0.0', '@1.0', '@1.0']]
    bayes_rate_dict = re_bayes_rate2re_rate(re_bayes_rate)
    print(bayes_rate_dict)
    # {(0, 0): ' 1 ', (0, 1): ' 1 ', (0, 2): '*', (1, 0): '@0.0', (1, 1): '@1.0', (1, 2): '@1.0'}
    re_rate_dict = fc['re_rate_dict']
    print(re_rate_dict)
    # {'(0, 0)': ' 1 ', '(0, 1)': '#0.25', '(1, 0)': ' 1 ', '(1, 1)': '#0.25', '(2, 0)': '#0.25', '(2, 1)': '#0.25'}

    diff_tuple, diff_minus_dict, diff_value = diff2value(bayes_rate_dict, re_rate_dict)
    print(diff_tuple)
    print(diff_value)
    # ({(0, 0): ' 1 ', (1, 0): '*', (2, 0): '@1.0', (0, 1): ' 0 ', (1, 1): '@1.0', (2, 1): '@0.0'},
    #  {'(0, 0)': ' 1 ', '(0, 1)': ' 0 ', '(1, 0)': '#0.25', '(1, 1)': '#0.25', '(2, 0)': '#0.25', '(2, 1)': '#0.25'})
    # 0.2916666666666667
    diff_content = {str(diff_tuple): diff_value}
    print(diff_content)
    diff_content_ls.append(diff_content)
    fc['bayes_rate_dict'] = bayes_rate_dict
    fc['diff_value'] = diff_value
    fc['diff_minus_dict'] = diff_minus_dict
    print(fc)
print(focus_content)
sorted_fo_content = sorted(focus_content, key=lambda d: -d['diff_value'])
print(sorted_fo_content)

if __name__ == '__main__':
    row_num = 2
    col_num = 3
    # total_reward = random_play_batch(row_num, col_num, init_reward=0, episode=1000)
    total_reward = play_batch(row_num, col_num, init_reward=0, episode=1000,record_flag=True,memo_path='memo.json')
    print(total_reward)
    print('random play win rate', total_reward / 1000)















