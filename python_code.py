# -*- coding: UTF-8 -*-
import datetime as dt
import time
import pickle
import os 
import sys
# ----------------------------------------------------
# python 运行时刷新缓冲区
sys.stdout.flush()
# python 运行时文件刷新缓冲区
fi = open("xxx.txt", "w")
fi.flush()
# ----------------------------------------------------
# python2 python3 的编码问题


# python2
# unicode 和 str互转 

# python2 中 两种字符串 str(utf-8编码的字节序列 兼容ascii) 你好 <--> unicode u你好  

#Python2.X如何将Unicode中文字符串转换成 string字符串
#普通字符串可以用多种方式编码成Unicode字符串，具体要看你究竟选择了哪种编码：
unicodestring = u"Hello world" 
# 将Unicode转化为普通Python字符串："encode"  
utf8string = unicodestring.encode("utf-8")  
asciistring = unicodestring.encode("ascii")  
# 将普通Python字符串转化为Unicode："decode"  
plainstring1 = unicode(utf8string,"utf-8")  
plainstring2 = unicode(asciistring,"ascii")  

# python3 
# python3 中的字符串全部是unicode unicode通过utf-8 转换为 bytes
bytes = "你好".encode("utf-8")
unicode_str = bytes.decode("utf-8")

# GBK <--> unicode <--> utf-8 互转  unicode 是中转   
# GBK 和 utf-8对应的都是 bytes 是用来存储在文件中的字节序列
# 可以理解为 unicode 可以通过不同方式编码为不同的字节序列（GBK字节序列 utf-8字节序列）
"你好".encode("GBK").decode("GBK")

# ----------------------------------------------------
# json相关
import json
json.load(open("xxx.json"))
json.loads("{\"A\":1 \"B\":2}")
json.dump(obj ,open("xxx.json","w"), ensure_ascii=False, sort_keys=True, indent=4) # ensure_ascii=False 选项可以保证输出可视的中文 
json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=4)


# ----------------------------------------------------
# time 相关
import time
time.time()


# ----------------------------------------------------
# datetime 相关
import datetime as dt 
dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


# ----------------------------------------------------
# 可视化进度条相关
from tqdm import tqdm
for i in tqdm(range(1000)):
    sleep(1)
    print("haha")


# ----------------------------------------------------
# log 相关 https://blog.csdn.net/hallo_ween/article/details/64906838

# LOGGING handler 对应的是是

import logging  # 引入logging模块

# --------------将信息打印到控制台上---------------------
logging.basicConfig(level=logging.NOTSET,format="%(asctime)s %(message)s")  # 设置日志级别 不设置默认为WARING以上


logging.debug(u"苍井空")
logging.info(u"麻生希")
logging.warning(u"小泽玛利亚")
logging.error(u"桃谷绘里香")
logging.critical(u"泷泽萝拉")


# --------------logging输出到文件----------------------
import logging  # 引入logging模块
# 第一步，创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关
# 第二步，创建一个handler，用于写入日志文件
fh = logging.FileHandler("test.log" ,mode='w')
fh2 = logging.FileHandler("test2.log", mode='w')
fh.setLevel(logging.ERROR)  # 输出到file的log等级的开关
fh2.setLevel(logging.INFO)  # 输出到file的log等级的开关

# 第三步，定义handler的输出格式


'''
属性名 格式  描述
asctime %(asctime)s 易读的时间格式： 默认情况下是2003-07-08 16：49：45896的形式（逗号之后的数字是毫秒部分的时间）
filename    %(filename)s    路径名的文件名部分。
funcName    %(funcName)s    日志调用所在的函数名
levelname   %(levelname)s   消息的级别名称(DEBUG INFO WARNING ERROR CRITICAL).
levelno %(levelno)s 对应数字格式的日志级别 (DEBUG INFO WARNING ERRORCRITICAL).
lineno  %(lineno)d  发出日志记录调用的源码行号 (如果可用)。
module  %(module)s  所在的模块名(如test6.py模块则记录test6)
message %(message)s 记录的信息
name    %(name)s    调用的logger记录器的名称
process %(process)d 进程ID
processName %(processName)s 进程名
thread  %(thread)d  线程ID
threadName  %(threadName)s  线程名
'''


formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
fh2.setFormatter(formatter)

# 第四步，将logger添加到handler里面
logger.addHandler(fh)  #可以向logger中添加不同配置的文件handler 来实现不同的输出
logger.addHandler(fh2)
# 日志
logger.debug("this is a logger debug message")
logger.info("this is a logger info message")
logger.warning("this is a logger warning message")
logger.error("this is a logger error message")
logger.critical("this is a logger critical message")

# ------------颜色日志 coloredlogs ------------------
# 安装 pip install coloredlogs
import coloredlogs logging
# 从logging获取logger
logger = logging.getLogger()

# 配置handler和logger
fh = logging.FileHandler("test.log",mode=w)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# 将颜色模块 安装到 logger上
coloredlogs.install(level=DEBUG,logger=logger)

# 输出日志
logger.debug('this is a logger debug message')
logger.info( 'this is a logger info message')
logger.warning('this is a logger warning message')
logger.error('this is a logger error message')
logger.critical('this is a logger critical message')


# --------------------------------------------------------

class ColorLogging:
    """
        分级别答应不同颜色的日志
    """

    def __init__(self):
        pass

    @staticmethod
    def getTimeStr():
        import datetime as dt
        return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
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

    @staticmethod
    def debug(info):
        if not isinstance(info, str):
            info = str(info)
        print(ColorLogging.colorStr("{level}: {time} {info}".format(level="DEBUG", time=ColorLogging.getTimeStr(), info=info), color="blue"))

    @staticmethod
    def info(info):
        if not isinstance(info, str):
            info = str(info)
        print(ColorLogging.colorStr("{level}: {time} {info}".format(level="INFO", time=ColorLogging.getTimeStr(), info=info), color="green"))

    @staticmethod
    def warn(info):
        if not isinstance(info, str):
            info = str(info)
        print(ColorLogging.colorStr("{level}: {time} {info}".format(level="WARNING", time=ColorLogging.getTimeStr(), info=info), color="yellow"))

    @staticmethod
    def error(info):
        if not isinstance(info, str):
            info = str(info)
        print(ColorLogging.colorStr("{level}: {time} {info}".format(level="ERROR", time=ColorLogging.getTimeStr(), info=info), color="red"))

    @staticmethod
    def critical(info):
        if not isinstance(info, str):
            info = str(info)
        print(ColorLogging.colorStr("{level}: {time} {info}".format(level="CRITICAL", time=ColorLogging.getTimeStr(), info=info), color="purple"))

