def po_plus_dire(row_num ,col_num,position, direction):

    for d in direction:
        if d == 'd':
            position = (position[0] + 1, position[1])
        if d == 'u':
            position = (position[0] - 1, position[1])
        if d == 'r':
            position = (position[0], position[1] + 1)
        if d == 'l':
            position = (position[0], position[1] - 1)

    print(position)
    if position[0] in range(row_num) and position[1] in range(col_num):
        return position
    else:
        return


def edr_value(re_sim_dict, position, mine_rate):
    re_sim_dict[position] = '?' + str(1 - float(mine_rate))
    return re_sim_dict





















