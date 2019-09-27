import datetime as dt
import time
import sys

def get_ts():
    return dt.datetime.now().timestamp()

def get_date():
    return dt.datetime.now().strftime("%Y%m%d")

while True:
    input_str = input("input your events with time, format: $event_name $event_maxtime(min)\n")
    if len(input_str) < 2:
        continue
    sep = input_str.split()
    event_name = sep[0]
    event_max_min = int(sep[1]) 
    event_maxtime = event_max_min * 60
    start_time = get_ts()
    SLEEP_INTERVAL = 20
    try:
        while True:
            cur_ts = get_ts()
            running_min = int(cur_ts - start_time) // 60
            sys.stdout.write("%s already running %03d minutes\r" % ("->" + event_name, running_min))
            sys.stdout.flush()
            time.sleep(SLEEP_INTERVAL)
            if running_min > event_max_min:
                break
        print("{0} time {1} minute up\n".format(event_name, event_max_min))
        with open("daily_event_{0}.log".format(get_date()), "a") as f:
            f.write("========================\n")
            f.write("{0} last for {1} minutes\n".format(event_name, running_min))
            f.flush()
    except KeyboardInterrupt:
        print("job end by hand")
        with open("daily_event_{0}.log".format(get_date()), "a") as f:
            f.write("========================\n")
            f.write("{0} last for {1} minutes\n".format(event_name, running_min))
            f.flush()