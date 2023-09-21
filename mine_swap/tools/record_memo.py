from mine_swap.tools.create_env import new_env, actual_env_4_raw, print_env, init_player_ob
from mine_swap.tools.random_play import sim_till_end_random
from mine_swap.tools.init_func import init_value
from mine_swap.tools.token_func import get_n_k,get_n_s
from mine_swap.tools.read_json import read_edr,read_theme,read_knowledge,read_edr_value
from mine_swap.tools.suspect import po_plus_dire,edr_value
import json, time


def random_play_batch(row_num, col_num, init_reward=0, episode=1000):
    total_reward = init_reward
    episode = episode
    for i in range(episode):
        print('=-----------------' + str(i) + '  episode=-----------------')
        env = new_env(row_num, col_num)
        print(env)
        raw_env = list(map(list, zip(*env)))
        print(raw_env)
        actual_env = actual_env_4_raw(raw_env)
        plob = init_player_ob(actual_env)
        print(plob)
        reward = sim_till_end_random(plob, actual_env)
        total_reward += reward
    return total_reward


def play_batch(row_num, col_num, init_reward=0, episode=1000,record_flag=False,memo_path='memo.json'):
    batch_reward = reward = init_reward
    episode = episode
    for i in range(episode):
        print('=-----------------' + str(i) + '  episode=-----------------')
        env, env_time_stamp = new_env(row_num, col_num)
        # print(env)
        raw_env = list(map(list, zip(*env)))
        # print(raw_env)
        actual_env = actual_env_4_raw(raw_env)
        plob = init_player_ob(actual_env)
        # print(plob)
        reward = sim_till_end(plob, actual_env,env_time_stamp, reward,record_flag=record_flag,memo_path=memo_path)
        batch_reward += reward
    return batch_reward


def value2rate(col_num, plob_ima, re_sim_dict_flag=False):
    if not re_sim_dict_flag:
        re_sim_dict = {(x, y): plob_ima[x][y] for x in range(len(plob_ima)) for y in range(len(plob_ima[x]))}
    else:
        re_sim_dict = plob_ima
    sum_value = sum([float(x[1:]) for x in re_sim_dict.values() if x.startswith('?')])

    mine_count = col_num - sum([1 for v in re_sim_dict.values() if v == '*'])

    unknow_num = sum([1 for x in re_sim_dict.values() if x.startswith('?')])

    re_rate_dict = dict((k, '#' + str(float(1 / unknow_num * mine_count))) if sum_value * mine_count == 0 else (
        k, '#' + str(float(v[1:]) / sum_value * mine_count)) if v.startswith('?') else (k, v) for k, v in
                        re_sim_dict.items())

    re_rate_select = dict((k, '#' + str(float(1 / unknow_num))) if sum_value == 0 else
                          (k, '#' + str(float(v[1:]) / sum_value)) if v.startswith('?') else (k, v) for k, v in
                          re_sim_dict.items())
    re_rate_select = dict(
        (k, '#10000000000') if v == '#0.0' else (k, '#' + str(1 / float(v[1:]))) if v[0] == '#' else (k, v) for (k, v)
        in re_rate_select.items())

    return re_rate_dict, re_rate_select


def select_rate(re_rate_dict):
    import random
    ra = random.random()
    for k, v in re_rate_dict.items():
        if v.startswith('#'):
            ra -= float(v[1:])
        if ra <= 0:
            return k
    return k


def record2memo(memo_path, actual_env, env_time_stamp, plob, knowledge_no, suspect_no, re_rate_dict, action,
                step,beneficial,reward):
    content = [{"plob": plob,
                "knowledge_no": knowledge_no,
                "suspect_current_no": suspect_no,
                "re_rate_dict": {str(k): v for k, v in re_rate_dict.items()},
                "action": str(action),
                "step": step,
                "beneficial": beneficial,
                "reward": reward}]

    all_content = {"actual_env": actual_env,
                   "env_time_stamp": env_time_stamp,

                   "content": content}
    try:
        with open(memo_path) as f:
            d = json.load(f)
            flag = True
            for record in d['record']:
                print(record)
                if record['actual_env'] == actual_env and record['env_time_stamp'] == env_time_stamp:
                    record['content'].extend(content)
                    flag = False
                    break
            if flag:
                d['record'].append(all_content)
            print(d)
    except:
        d = {
            "record": [
            ]
        }
        d['record'].append(all_content)
    with open(memo_path, 'w') as f:
        json.dump(d, f)


def value_by_conjecture(plob, knowledge_no,edr_path='edr.json',knowledge_path='knowledge.json'):
    """stratige based on knowledge"""

    d_edr = read_edr()
    print(d_edr)

    d_knowledge = read_knowledge()
    print(d_knowledge)

    plob_ima = [[y + str(1) if y.startswith('?') else y for y in x] for x in plob]
    print(plob_ima)
    re_sim_dict = {(x, y): plob_ima[x][y] for x in range(len(plob_ima)) for y in range(len(plob_ima[x]))}
    print(re_sim_dict)

    for edr_no in d_knowledge[str(knowledge_no)]:
        print(edr_no)
        print(type(d_edr))
        print(type(edr_no))
        edr = eval(d_edr[str(edr_no)])
        print(edr)
        print(type(edr))
        # {(('2', ''), '2'): {('2', 'l'): ('*', 1.0)}}
        key_num = list(list(edr.values())[0].keys())[0][0]
        direction = list(list(edr.values())[0].keys())[0][1]
        mine_rate = list(list(edr.values())[0].values())[0][1]

        arr = [k for k, v in re_sim_dict.items() if v == key_num]
        print(arr)
        for position in arr:
            position = po_plus_dire(position, direction)
            if position:
                re_sim_dict = edr_value(re_sim_dict, position, mine_rate)
                print(re_sim_dict)
    return re_sim_dict


def sim_till_end(plob,actual_env,env_time_stamp, reward, step=1,record_flag=False, conjecture=False,knowledge_no='',suspect_no='',memo_path='memo.json'):
    """ simulate one game , until get reward """
    plob_ima = init_value(plob)
    col_num = len(plob[0])
    if conjecture:
        re_sim_dict = value_by_conjecture(plob, knowledge_no)
        re_rate_dict, re_rate_select = value2rate(col_num,re_sim_dict, re_sim_dict_flag=True)
        a, b = action = select_rate(re_rate_dict)

    else:
        re_rate_dict, re_rate_select = value2rate(col_num,plob_ima)
        a, b = action = select_rate(re_rate_dict)
    plob[a][b] = actual_env[a][b]
    beneficial = 0
    continue_flag = True
    success_reward = 0
    failure_reward = -1
    # total_reward = 0

    if actual_env[a][b] == '*':
        continue_flag = False
        # print('game  over  ...  ')
        # raw_show(actual_env, 'actual_env')
        beneficial = failure_reward
        reward += beneficial

    elif sum([str(x).count('?') for y in plob for x in y]) == len(plob[0]):
        continue_flag = False
        # print('game  successed  ...  ')
        beneficial = success_reward
        reward += beneficial
    else:
        pass

    if record_flag:
        record2memo(memo_path, actual_env, env_time_stamp, plob, knowledge_no, suspect_no, re_rate_dict, action,
                    step,beneficial,reward)

    if continue_flag:
        step+=1
        reward = sim_till_end(plob, actual_env,env_time_stamp, reward,step,record_flag=record_flag, conjecture=conjecture,knowledge_no=knowledge_no,suspect_no=suspect_no,memo_path=memo_path)

    return reward


if __name__ == '__main__':
    row_num = 2
    col_num = 3
    # total_reward = random_play_batch(row_num, col_num, init_reward=0, episode=1000)
    total_reward = play_batch(row_num, col_num, init_reward=0, episode=1000,record_flag=True,memo_path='memo.json')
    print(total_reward)
    print('random play win rate', total_reward / 1000)
