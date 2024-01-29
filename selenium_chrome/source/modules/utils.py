from datetime import datetime

def is_in_update_graph():
    now = datetime.now()
    time_str = now.strftime("%H:%M")
    minute = int(time_str.split(":")[1])
    return minute % 10 in [0, 1, 2, 3, 4]
