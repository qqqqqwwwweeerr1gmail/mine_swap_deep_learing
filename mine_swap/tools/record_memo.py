from mine_swap.tools.create_env import new_env, actual_env_4_raw, print_env, init_player_ob
from mine_swap.tools.random_play import sim_till_end


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
        reward = sim_till_end(plob, actual_env)
        total_reward += reward
    return total_reward


if __name__ == '__main__':
    row_num = 3
    col_num = 3
    total_reward = random_play_batch(row_num, col_num, init_reward=0, episode=1000)
    print(total_reward)
    print('random play win rate', total_reward / 1000)
