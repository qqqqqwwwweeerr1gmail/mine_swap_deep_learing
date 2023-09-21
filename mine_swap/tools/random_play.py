from mine_swap.tools.create_env import new_env,actual_env_4_raw,print_env,init_player_ob
import random

def strategy_random_select(plob):
    rd = random.random()
    s = sum([str(x).count('?') for y in plob for x in y])
    if s == 4:
        print('----remian----', s)
    if s == 3:
        print('----remian----', s)

    ob_dict = {(x, y): plob[x][y] for x in range(len(plob)) for y in range(len(plob[x]))}
    all_select_possible = {k: v for k, v in ob_dict.items() if v == '?'}
    rs = random.choice(list(all_select_possible))
    return rs


def sim_till_end_random(plob, actual_env):
    print('------------------sim_till_end----------------------')
    print_env(plob, name='before_select plob')
    a, b = strategy_random_select(plob)
    print('action select : row col ', a, b)

    print_env(actual_env, name='actual env:')
    plob[a][b] = actual_env[a][b]
    print_env(plob, name='after_select plob')
    if actual_env[a][b] == '*':

        print('game  over  ...  ')
        return 0
    elif sum([str(x).count('?') for y in plob for x in y]) == len(plob[0]):

        print('game  successed  ...  ')
        return 1
    else:
        return sim_till_end_random(plob, actual_env)


def random_play(row_num,col_num):
    env = new_env(row_num, col_num)
    raw_env = list(map(list, zip(*env)))
    actual_env = actual_env_4_raw(raw_env)
    plob = init_player_ob(actual_env)
    sim_till_end_random(plob, actual_env)



if __name__ == '__main__':
    row_num = 2
    col_num = 3
    random_play(row_num, col_num)

















