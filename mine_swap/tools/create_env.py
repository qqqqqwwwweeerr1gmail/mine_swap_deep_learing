import time

def new_row(row_num):
    #  rule  1
    import random
    # print(random.random() * row_num)
    minder = int(random.random() * row_num)
    # print(minder)
    row = [0 if x == minder else 1 for x in range(row_num)]
    # print(row)
    return row


def new_env(row_num,col_num):
    env = []
    #  firstnoneminer
    env.append([1, *new_row(row_num - 1)])
    for i in range(1, col_num):
        env.append(new_row(row_num))
    # print(env)
    env_time_stamp = int(time.time() * 1_000_000)
    return env, env_time_stamp

def raw_show(show_env, name=''):
    print(name + ' ...')
    for row in range(len(show_env)):
        for col in range(len(show_env[row])):
            print(' ' + show_env[row][col].replace(' ', '') + ' ', end='')
        print()

# def show_and_count(show_env, name='actual_world', re=False):
#     # for row in range(len(show_env)):
#     #     for col in range(len(show_env[row])):
#     #         if show_env[row][col] == 1:
#     #             print(' 0 ', end='')
#     #         if show_env[row][col] == 0:
#     #             print(' * ', end='')
#     #     print()
#     print(name + ' ...')
#     actual_env = []
#     for row in range(len(show_env)):
#         actual_row_arr = []
#         for col in range(len(show_env[row])):
#             if show_env[row][col] == 1:
#                 actual_row_arr.append(count_cheractor(show_env, row, col))
#                 print(count_cheractor(show_env, row, col), end='')
#             if show_env[row][col] == 0:
#                 actual_row_arr.append('*')
#                 print(' * ', end='')
#             if show_env[row][col] == '?':
#                 actual_row_arr.append('?')
#                 print(' ? ', end='')
#         actual_env.append(actual_row_arr)
#         print()
#     if re:
#         return actual_env

def actual_env_4_raw(raw_env):
    actual_env = []
    for row in range(len(raw_env)):
        actual_row_arr = []
        for col in range(len(raw_env[row])):
            if raw_env[row][col] == 1:
                actual_row_arr.append(count_cheractor(raw_env, row, col))
                # print(count_cheractor(show_env, row, col), end='')
            if raw_env[row][col] == 0:
                actual_row_arr.append('*')
                # print(' * ', end='')
            if raw_env[row][col] == '?':
                actual_row_arr.append('?')
                # print(' ? ', end='')
        actual_env.append(actual_row_arr)
    return actual_env

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

def init_player_ob(actual_env):
    plob = [['?' for x in y] for y in actual_env]
    plob[0][0] = actual_env[0][0]
    return plob

def print_env(show_env, name=''):
    print(name + ' ...')
    for row in range(len(show_env)):
        for col in range(len(show_env[row])):
            print(' ' + show_env[row][col].replace(' ', '') + ' ', end='')
        print()


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

















