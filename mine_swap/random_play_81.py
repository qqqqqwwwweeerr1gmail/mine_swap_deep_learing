import random

env = []


def new_row(row_num):
    #  rule  1
    import random
    print(random.random() * row_num)
    minder = int(random.random() * row_num)
    print(minder)
    row = [0 if x == minder else 1 for x in range(row_num)]
    print(row)
    return row


def new_env(row_num,col_num):
    env = []
    #  firstnoneminer
    env.append([1, *new_row(row_num - 1)])
    for i in range(1, col_num):
        env.append(new_row(row_num))
    print(env)
    return env


def count_cheractor(env, row, col):
    character = '01234'
    k = 0

    #  left
    if col > 0 and env[row][col - 1] == 0:
        k += 1
    #  down
    if row < len(env) - 1 and env[row + 1][col] == 0:
        k += 1
    #  right
    if col < len(env[row]) - 1 and env[row][col + 1] == 0:
        k += 1
    #  up
    if row > 0 and env[row - 1][col] == 0:
        k += 1
    return ' ' + character[k] + ' '


def raw_show(show_env, name=''):
    print(name + ' ...')
    for row in range(len(show_env)):
        for col in range(len(show_env[row])):
            print(' ' + show_env[row][col].replace(' ', '') + ' ', end='')
        print()


def show_and_count(show_env, name='actual_world', re=False):
    for row in range(len(show_env)):
        for col in range(len(show_env[row])):
            if show_env[row][col] == 1:
                print(' 0 ', end='')
            if show_env[row][col] == 0:
                print(' * ', end='')
        print()
    print(name + ' ...')
    actual_env = []
    for row in range(len(show_env)):
        actual_row_arr = []
        for col in range(len(show_env[row])):
            if show_env[row][col] == 1:
                actual_row_arr.append(count_cheractor(show_env, row, col))
                print(count_cheractor(show_env, row, col), end='')
            if show_env[row][col] == 0:
                actual_row_arr.append('*')
                print(' * ', end='')
            if show_env[row][col] == '?':
                actual_row_arr.append('?')
                print(' ? ', end='')
        actual_env.append(actual_row_arr)
        print()
    if re:
        return actual_env


def init_player_ob(actual_env):
    plob = [['?' for x in y] for y in actual_env]
    plob[0][0] = actual_env[0][0]
    return plob
    #  none  random


def strategy(plob):
    #  print(plob)
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


def sim_till_end(plob,actual_env):
    print('------------------sim_till_end----------------------')
    raw_show(plob, name='before_select plob')
    global total_reward
    a, b = strategy(plob)
    print(a, b)

    raw_show(actual_env)
    plob[a][b] = actual_env[a][b]
    raw_show(plob, name='after_select plob')
    if actual_env[a][b] == '*':

        print('game  over  ...  ')
    elif sum([str(x).count('?') for y in plob for x in y]) == len(plob[0]):

        print('game  successed  ...  ')

        total_reward += 1
    else:

        sim_till_end(plob,actual_env)


def random_play_sim(row_num,col_num,init_reward,episode):
    col_num = col_num
    row_num = row_num
    global total_reward
    total_reward = init_reward
    episode = episode
    for i in range(episode):
        print('=-----------------'+str(i)+'  episode=-----------------')
        env = new_env(row_num,col_num)
        print(env)
        raw_env = list(map(list, zip(*env)))
        print(raw_env)
        actual_env = show_and_count(raw_env, re=True, name='raw_env')
        plob = init_player_ob(actual_env)
        print(plob)
        #  print(actual_env)
        #  show(plob,  name='plob'
        #  print(actual_env)
        # raw_show(plob, name='plob')

        sim_till_end(plob,actual_env)
if __name__ == '__main__':
    total_reward = 0
    episode = 10000
    random_play_sim(row_num=3, col_num=3, init_reward=0, episode=episode)
    print(total_reward)
    print('random play win rate',total_reward / episode)
