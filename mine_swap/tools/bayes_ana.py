from mine_swap.tools.content_ana import get_bf_plob, init_value


def re_shuffle2col(plob):
    """flip row to col """
    re_plob = [[plob[y][x] for y in range(len(plob))] for x in range(len(plob[0]))]
    return re_plob


def fill_mine(re_plob):
    import random, copy

    re_sim_env = []
    for col in re_plob:
        if '*' in col:
            temp_row = copy.deepcopy(col)
            re_sim_env.append(temp_row)
            continue
        ob_dict = {(x, y): col[x][y] for x in range(len(col)) for y in range(len(col[x]))}
        all_select_possible = {k: v for k, v in ob_dict.items() if v == '?'}
        # rs = random.choice(list(all_select_possible))
        a, b = random.choice(list(all_select_possible))
        temp_row = copy.deepcopy(col)
        temp_row[a] = '*'
        re_sim_env.append(temp_row)
    return re_sim_env


def re2dict(re_sim_env):
    ob_dict = {(x, y): re_sim_env[x][y] for x in range(len(re_sim_env)) for y in range(len(re_sim_env[x]))}
    return ob_dict


def check_cop_re(re_sim_env):
    re_sim_env = [[y.replace(' ', '') for y in x] for x in re_sim_env]
    # print(re_sim_env)
    re_sim_dict = re2dict(re_sim_env)
    # print(re_sim_dict)
    all_num_position = {k: v for k, v in re_sim_dict.items() if v in '01234'}
    # print(all_num_position)
    for k, v in all_num_position.items():
        a, b = k
        print(a, b)
        # check if mine in left/down/right/up
        mine_num = 0
        mine_num += 1 if (a, b - 1) in re_sim_dict and re_sim_dict[(a, b - 1)] == '*' else 0
        mine_num += 1 if (a - 1, b) in re_sim_dict and re_sim_dict[(a - 1, b)] == '*' else 0
        mine_num += 1 if (a, b + 1) in re_sim_dict and re_sim_dict[(a, b + 1)] == '*' else 0
        mine_num += 1 if (a + 1, b) in re_sim_dict and re_sim_dict[(a + 1, b)] == '*' else 0
    if int(v) != mine_num:
        return False
    return True


def bayes_sim(re_plob):
    '''bayes sim is based on current view , sim one possible current situation randomly with MC methods'''

    '''
    rules_check
    1. only one mine on each line
    2. corporate with the showing num
    then count another num
    '''
    re_sim_env = fill_mine(re_plob)
    while not check_cop_re(re_sim_env):
        re_sim_env = fill_mine(re_plob)
    print(re_sim_env)
    re_sim_env = fill_mum(re_sim_env)
    return re_sim_env


def dict2arr(re_sim_dict):
    arr = []
    row = []
    temp_row_num = 0
    for k, v in re_sim_dict.items():
        a, b = k

        if temp_row_num != a:
            arr.append(row)
            temp_row_num = a
            row = []
        row.append(v)
    arr.append(row)
    return arr


def fill_mum(re_sim_env):
    # print(re_sim_env)
    re_sim_dict = {(x, y): re_sim_env[x][y] for x in range(len(re_sim_env)) for y in range(len(re_sim_env[x]))}
    all_select_possible = {k: v for k, v in re_sim_dict.items() if v == '?'}

    print(re_sim_dict)
    # print(all_select_possible)

    for k, v in all_select_possible.items():
        a, b = k
        # check if mine in left/down/right/up
        mine_num = 0
        mine_num += 1 if (a, b - 1) in re_sim_dict and re_sim_dict[(a, b - 1)] == '*' else 0
        mine_num += 1 if (a - 1, b) in re_sim_dict and re_sim_dict[(a - 1, b)] == '*' else 0
        mine_num += 1 if (a, b + 1) in re_sim_dict and re_sim_dict[(a, b + 1)] == '*' else 0
        mine_num += 1 if (a + 1, b) in re_sim_dict and re_sim_dict[(a + 1, b)] == '*' else 0
        re_sim_dict[a, b] = str(mine_num)
    re_sim_env = dict2arr(re_sim_dict)
    return re_sim_env


def bayes_mine_value(plob, epoch):
    re_plob = re_shuffle2col(plob)
    # [['1', '?', '?'], ['0', '?', '?']]
    re_bayes_ima = [['$' if y.startswith('?') else y for y in x] for x in re_plob]
    print(re_bayes_ima)
    # [['1', '$', '$'], ['0', '$', '$']]
    for i in range(epoch):
        re_sim_env = bayes_sim(re_plob)
        print(re_sim_env)
        # [['1', '*', '2'], ['0', '2', '*']]
        re_bayes_ima = [
            [re_bayes_ima[x][y] + re_sim_env[x][y] if re_bayes_ima[x][y][0] == '$' else re_bayes_ima[x][y] for y in
             range(len(re_bayes_ima[x]))] for x in range(len(re_bayes_ima))]
        # [['1', '$*', '$2'], ['0', '$2', '$*']]

    return re_bayes_ima


def bayes_mine_rate(bayes_ima):
    bayes_rate = [
        ['@' + str(sum([0 if x.isnumeric() else 1 for x in y[1:]]) / int(len(y[1:]))) if y.startswith('$') else y for y
         in x] for x in bayes_ima]
    return bayes_rate


def re_bayes_rate2re_rate(re_bayes_rate):
    bayes_rate_dict = {(y, x): re_bayes_rate[x][y] for x in range(len(re_bayes_rate)) for y in
                       range(len(re_bayes_rate[x]))}
    return bayes_rate_dict


def diff2value(bayes_rate_dict, re_rate_dict):
    diff_tuple = (bayes_rate_dict, re_rate_dict)
    diff_minus_dict = dict(
        (k, round(abs(float(v[1:]) - float(re_rate_dict[str(k)][1:])),4)) if v.startswith('@') else (k, v) for k, v in
        bayes_rate_dict.items())
    diff_value = round(sum([x if type(x) == float else 0 for x in diff_minus_dict.values()]) / len(diff_minus_dict),4)
    return diff_tuple, diff_minus_dict, diff_value


def content_diff_sorted(focus_content, bayes_epoch=1000):
    diff_content_ls = []
    for fc in focus_content:
        plob = fc['plob']
        action = fc['action']
        print(plob)
        print(action)
        # [[' 1 ', '?'], [' 1 ', '?'], ['*', '?']]
        # (2, 0)
        bf_plob = get_bf_plob(plob, action)
        print('bf_plob : ', bf_plob)
        # [[' 1 ', '?'], [' 1 ', '?'], ['?', '?']]

        plob_ima = init_value(bf_plob)
        print('plob_ima : ', plob_ima)  # is select value
        # [[' 1 ', '?0.1'], [' 1 ', '?0.1'], ['?0.1', '?0.1']]
        re_bayes_ima = bayes_mine_value(plob, bayes_epoch)
        print('re_bayes_ima : ', re_bayes_ima)
        # [['1', '$11****1111', '$**2222****'], ['0', '$1122221111', '$**********']]
        re_bayes_rate = bayes_mine_rate(re_bayes_ima)
        print('re_bayes_rate : ', re_bayes_rate)
        # [['1', '@0.51', '@0.49'], ['0', '@1.0', '@0.0']]
        bayes_rate_dict = re_bayes_rate2re_rate(re_bayes_rate)
        print('bayes_rate_dict : ', bayes_rate_dict)
        # {(0, 0): '1', (1, 0): '@0.51', (2, 0): '@0.49', (0, 1): '0', (1, 1): '@1.0', (2, 1): '@0.0'}
        re_rate_dict = fc['re_rate_dict']
        print('re_rate_dict : ', re_rate_dict)  # action rate from memo
        # {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.5', '(1, 1)': '#0.5', '(2, 0)': '#0.5', '(2, 1)': '#0.5'}
        diff_tuple, diff_minus_dict, diff_value = diff2value(bayes_rate_dict, re_rate_dict)
        print('diff_tuple : ', diff_tuple)
        print('diff_minus_dict : ', diff_minus_dict)
        print('diff_value : ', diff_value)
        diff_content = {str(diff_tuple): diff_value}
        print(diff_content)
        diff_content_ls.append(diff_content)
        fc['bayes_rate_dict'] = bayes_rate_dict
        fc['diff_value'] = diff_value
        fc['diff_minus_dict'] = diff_minus_dict
        # break


    print(focus_content)
    sorted_fo_content = sorted(focus_content, key=lambda d: -d['diff_value'])
    print(sorted_fo_content)
    return sorted_fo_content


if __name__ == '__main__':

    focus_content = [{'plob': [['1', '0'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '0'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['2', '*'], ['?', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '1'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '1', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['?', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '#0.5', '(1, 1)': '1',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '0'], ['*', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.6666666666666666', '(1, 1)': '2',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['2', '*'], ['?', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.5', '(1, 0)': '#0.5', '(1, 1)': '2',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['2', '*'], ['?', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['0', '1'], ['?', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '1', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['0', '1'], ['2', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '1', '(1, 0)': '2', '(1, 1)': '#0.6666666666666666',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['0', '0'], ['1', '?'], ['*', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '0', '(1, 0)': '1', '(1, 1)': '#0.6666666666666666',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(2, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['2', '?'], ['*', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.5', '(1, 0)': '#0.5', '(1, 1)': '2',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '0'], ['*', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.6666666666666666', '(1, 1)': '2',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '0'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['2', '*'], ['?', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['0', '1'], ['2', '?'], ['*', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '1', '(1, 0)': '2', '(1, 1)': '#0.6666666666666666',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(2, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['0', '1'], ['2', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '1', '(1, 0)': '2', '(1, 1)': '#0.6666666666666666',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['2', '*'], ['?', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.5', '(1, 0)': '#0.5', '(1, 1)': '2',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '0'], ['*', '2'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.6666666666666666', '(1, 1)': '2',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['?', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['?', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '#0.5', '(1, 1)': '1',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '1'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['1', '1'], ['*', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(2, 0)', 'beneficial': -1},
                     {'plob': [['0', '?'], ['2', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '#0.5', '(1, 0)': '2', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '1'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '1', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['0', '?'], ['2', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '#0.5', '(1, 0)': '2', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['1', '1'], ['*', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.6666666666666666', '(1, 0)': '1', '(1, 1)': '1',
                                       '(2, 0)': '#0.6666666666666666', '(2, 1)': '#0.6666666666666666'},
                      'action': '(2, 0)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['1', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1},
                     {'plob': [['0', '?'], ['2', '*'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '0', '(0, 1)': '#0.5', '(1, 0)': '2', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(1, 1)', 'beneficial': -1},
                     {'plob': [['1', '*'], ['1', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '1', '(0, 1)': '#0.5', '(1, 0)': '1', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'}, 'action': '(0, 1)', 'beneficial': -1},
                     {'plob': [['2', '?'], ['*', '?'], ['?', '?']], 'knowledge': '', 'suspect_current': '',
                      're_rate_dict': {'(0, 0)': '2', '(0, 1)': '#0.4', '(1, 0)': '#0.4', '(1, 1)': '#0.4',
                                       '(2, 0)': '#0.4', '(2, 1)': '#0.4'}, 'action': '(1, 0)', 'beneficial': -1}]

    sorted_fo_content = content_diff_sorted(focus_content, bayes_epoch=1000)

{'plob': [['1', '0'], ['*', '?'], ['?', '?']],
 'knowledge': '',
 'suspect_current': '',
're_rate_dict': {'(0, 0)': '1', '(0, 1)': '0', '(1, 0)': '#0.5', '(1, 1)': '#0.5',
                                       '(2, 0)': '#0.5', '(2, 1)': '#0.5'},
 'action': '(1, 0)', 'beneficial': -1},


