import sys
import datetime as dt
import pandas as pd
from pyspark.sql import SparkSession, DataFrameWriter, Row, DataFrame
from pyspark import SparkConf

def initSpark(glbVars, appName="dafault_spark_job_songziheng"):
    """
    初始化spark环境
    :return:
    """
    current_time = dt.datetime.now()
    current_time.strftime("%Y-%m-%d %H:%M")
    warehouse_location = "/user/tiger/warehouse"
    conf = (SparkConf().setAppName(appName + current_time.strftime("%Y-%m-%d %H:%M"))
            .set("spark.sql.warehouse.dir", warehouse_location)
            .set("total-executor-cores", "1000")
            .set("spark.executor.cores", "1")
            .set("spark.speculation", "true")
            .set("spark.dynamicAllocation.enabled", "true")
            .set("spark.dynamicAllocation.initialExecutors", "550")
            .set("spark.dynamicAllocation.minExecutors", "500")
            .set("spark.dynamicAllocation.maxExecutors", "600")
            .set("spark.executor.memory", "16g")
            .set("spark.driver.maxResultSize", "10g")
            .set("spark.yarn.executor.memoryOverhead", "16g")
            .set("spark.driver.memory", "16g")
            )
    spark = (SparkSession
             .builder
             .config(conf=conf)
             .enableHiveSupport()
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
    glbVars["SparkSession"] = spark
    return spark

def unionAll(dfs):
    return reduce(DataFrame.union, dfs)

def readCsvs(pathTemplate, iterator):
    dfs = []
    for part in iterator:
        path = pathTemplate.format(part)
        df = spark.read.csv(path, header=True, inferSchema=True)
        dfs.append(df)
    return unionAll(dfs)

def showInfo(info="non", color="greenblue"):
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
        "red":      '\033[1;31;40m {0} \033[0m',
        "green":    '\033[1;32;40m {0} \033[0m',
        "yellow":   '\033[1;33;40m {0} \033[0m',
        "blue":     '\033[1;34;40m {0} \033[0m',
        "purple":   '\033[1;35;40m {0} \033[0m',
        "greenblue":'\033[1;36;40m {0} \033[0m',
        "white":    '\033[1;37;40m {0} \033[0m',
    }
    if color is None:
        print "{0} INFO:".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M")) + "  " + info
    else:
        print colorStr[color].format("{0} INFO:".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M")) + "  " + info)
