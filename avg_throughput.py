import matplotlib.pyplot as plt

UNLOCK_PIN = 18

def calculate_total_time(lines):
    """
    Output a time in seconds.
    """
    time = 0
    for line in lines:
        time += int(line[:-4])
    return time / (10 ** 6)


def count_packets_between_unlock(lines, pin_num: int):
    time = 0
    result = []
    num_packets = 0
    for line in lines:
        time += int(line[:-4])
        if int(line[-3: -1]) == UNLOCK_PIN:
            result.append((num_packets / time) * 10**6)
            time = 0
            num_packets = 0
        elif int(line[-3: -1]) == pin_num:
            num_packets += 1
    return result


def count_num_packets(lines, pin_num: int):
    num_packets = 0
    for line in lines:
        if int(line[-3: -1]) == pin_num:
            num_packets += 1
    return num_packets


if __name__ == "__main__":
    with open('./output_150000_cw_aggr_0312.dat') as ptr:
        lines =  ptr.readlines()
    lines = [line[line.find(']')+1:].strip() for line in lines]
    left = count_packets_between_unlock(lines, 22)
    mid = count_packets_between_unlock(lines, 27)
    right = count_packets_between_unlock(lines, 17)
    x_axis = [i for i in range(len(left))]
    plt.plot(x_axis, left, 'ro', label='left')
    plt.plot(x_axis, right, 'go',label='right')
    plt.plot(x_axis, mid, 'bo', label='mid')
    for i in range(len(left)):
        plt.axvline(x_axis[i] + 0.5)
    plt.legend()

    total_time = calculate_total_time(lines)
    print(total_time)

    avg_func = lambda pin,name:print(f'avg throughput for {name} is {count_num_packets(lines, pin)/total_time}pps')
    avg_func(27, "mid")
    avg_func(22, "left")
    avg_func(17, "right")



    # plt.show()
    