def is_in_update_graph(now_str):
    minute = int(now_str.split(":")[2])
    return minute % 10 in [0, 1, 2, 3, 4]
