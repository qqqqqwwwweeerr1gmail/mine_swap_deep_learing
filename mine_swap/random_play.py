
col_num = 2
row_num = 3

def new_row(row_num):
    # rule 1
    import random

    minder = int(random.random() * row_num)
    row = [0 if x == minder else 1 for x in range(row_num)]
    return row

def new_env():
    env = []
    # firstnoneminer
    env.append([1, *new_row(row_num - 1)])
    for i in range(1, col_num):
        env.append(new_row(row_num))
    return env

def show_and_count(show_env, name='actual_world', re=False):
    for row in range(len(show_env)):
        for col in range(len(show_env[row])):
            if show_env[row][col] == 1:
                pass
            if show_env[row][col] == 0:
                pass
    actual_env = []
    for row in range(len(show_env)):
        actual_row_arr = []
        for col in range(len(show_env[row])):
            if show_env[row][col] == 1:
                actual_row_arr.append(count_cheractor(show_env, row, col))
            if show_env[row][col] == 0:
                actual_row_arr.append('*')
            if show_env[row][col] == '?':
                actual_row_arr.append('?')
        actual_env.append(actual_row_arr)
    if re:
        return actual_env

def count_cheractor(env, row, col):
    character = '01234'
    k = 0
    # left
    if col > 0 and env[row][col - 1] == 0:
        k += 1
    # down
    if row < len(env) - 1 and env[row + 1][col] == 0:
        k += 1
    # right
    if col < len(env[row]) - 1 and env[row][col + 1] == 0:
        k += 1
    # up
    if row > 0 and env[row - 1][col] == 0:
        k += 1
    # return ' ' + character[k] + ' '
    return character[k]


env = new_env()
raw_env = list(map(list, zip(*env)))
actual_env = show_and_count(raw_env, re=True, name='raw_env')




































