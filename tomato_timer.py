import datetime as dt
import time
import sys
import tqdm
import os


def colorStr(str0, color="yellow", highlight=True):
    """
    -------------------------------------------
    -------------------------------------------
    字体色     |       背景色     |      颜色描述
    -------------------------------------------
    30        |        40       |       黑色
    31        |        41       |       红色
    32        |        42       |       绿色
    33        |        43       |       黃色
    34        |        44       |       蓝色
    35        |        45       |       紫红色
    36        |        46       |       青蓝色
    37        |        47       |       白色
    -------------------------------------------
    :param info:
    :param color:
    :return:
    """
    colorStr = {
        "red":      '\033[{highlight};31;40m {str0} \033[0m',
        "green":    '\033[{highlight};32;40m {str0} \033[0m',
        "yellow":   '\033[{highlight};33;40m {str0} \033[0m',
        "blue":     '\033[{highlight};34;40m {str0} \033[0m',
        "purple":   '\033[{highlight};35;40m {str0} \033[0m',
        "greenblue":'\033[{highlight};36;40m {str0} \033[0m',
        "white":    '\033[{highlight};37;40m {str0} \033[0m',
    }

    return colorStr[color].format(highlight= 1 if highlight else 0, str0=str0)

def get_ts():
    return dt.datetime.now().timestamp()

def get_date():
    return dt.datetime.now().strftime("%Y%m%d")

if __name__ == "__main__":
    pwd = os.getcwd()
    while True:
        input_str = input("input your events with time, format: $event_name $event_maxtime(min)\n")
        if len(input_str) < 2:
            continue
        sep = input_str.split()
        event_name = sep[0]
        event_max_min = int(sep[1]) 
        event_maxtime = event_max_min * 60
        start_time = get_ts()
        end_time_str = dt.datetime.now().strftime("%Y%m%d-%H:%M")
        SLEEP_INTERVAL = 10
        try:
            print(colorStr("{0} time {1} minute up @ %s \n".format(event_name, event_max_min, end_time_str), "red"))
            while True:
                cur_ts = get_ts()
                running_min = int(cur_ts - start_time) // 60
                sys.stdout.write("%s already running %s minutes\r" % ("-> " + colorStr(event_name, "yellow"), colorStr("%3d" % running_min, "green")))
                sys.stdout.flush()
                time.sleep(SLEEP_INTERVAL)
                if running_min >= event_max_min:
                    break 
                #slots = event_maxtime // SLEEP_INTERVAL
                #print("slot", slots)
                #for i in tqdm.tqdm(range(slots)):
                #    time.sleep(SLEEP_INTERVAL)
            print("\n!!!!\n")
            end_time_str = dt.datetime.now().strftime("%Y%m%d-%H:%M")
            print(colorStr("{0} time {1} minute up @ %s \n".format(event_name, event_max_min, end_time_str), "red"))
            
            with open("{0}/daily_event_{1}.log".format(pwd, get_date()), "a") as f:
                f.write("========================\n")
                f.write("{0} last for {1} minutes start@ {2} end@ {3} \n".format(event_name, running_min, strat_time_str, end_time_str))
                f.flush()
        except KeyboardInterrupt:
            print("job end by hand")
            with open("{0}/daily_event_{0}.log".format(pwd, get_date()), "a") as f:
                f.write("========================\n")
                f.write("{0} last for {1} minutes\n".format(event_name, running_min))
                f.flush()



