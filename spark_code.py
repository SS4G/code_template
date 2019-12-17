import sys
import datetime as dt
import pandas as pd
from pyspark.sql import SparkSession DataFrameWriter Row DataFrame
from pyspark import SparkConf

def initSpark(glbVars appName="dafault_spark_job_songziheng"):
    """
    初始化spark环境
    :return:
    """
    current_time = dt.datetime.now()
    current_time.strftime("%Y-%m-%d %H:%M")
    warehouse_location = "/user/tiger/warehouse"
    conf = (SparkConf().setAppName(appName + current_time.strftime("%Y-%m-%d %H:%M"))
            .set("spark.sql.warehouse.dir" warehouse_location)
            .set("total-executor-cores" "1000")
            .set("spark.executor.cores" "1")
            .set("spark.speculation" "true")
            .set("spark.dynamicAllocation.enabled" "true")
            .set("spark.dynamicAllocation.initialExecutors" "550")
            .set("spark.dynamicAllocation.minExecutors" "500")
            .set("spark.dynamicAllocation.maxExecutors" "600")
            .set("spark.executor.memory" "16g")
            .set("spark.driver.maxResultSize" "10g")
            .set("spark.yarn.executor.memoryOverhead" "16g")
            .set("spark.driver.memory" "16g")
            )
    spark = (SparkSession
             .builder
             .config(conf=conf)
             .enableHiveSupport()
             .getOrCreate())
    spark.sparkContext.setLogLevel("ERROR")
    glbVars["SparkSession"] = spark
    return spark

def unionDataFrameList(dfs):
    """
    将一个list中所有的DataFrame （需要保证schema相同）union起来为一个DataFrame
    适用于分桶后的操作 
    """
    return reduce(DataFrame.union dfs)

def readCsvs(pathList):
    """
    将一个pathList(一系列hdfs-csv)中所有的csv合并生成一个DataFrame （需要保证schema相同）union起来为一个DataFrame
    适用于分桶后的操作 
    """
    dfs = []
    for path in pathList:
        df = spark.read.csv(path header=True inferSchema=True)
        dfs.append(df)
    return unionDataFrameList(dfs)

def showInfo(info="NULL" color="greenblue"):
    """
    按照设置的颜色打印信息
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
        "red":      \033[1;31;40m {0} \033[0m
        "green":    \033[1;32;40m {0} \033[0m
        "yellow":   \033[1;33;40m {0} \033[0m
        "blue":     \033[1;34;40m {0} \033[0m
        "purple":   \033[1;35;40m {0} \033[0m
        "greenblue":\033[1;36;40m {0} \033[0m
        "white":    \033[1;37;40m {0} \033[0m
    }
    if color is None:
        print "{0} INFO:".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M")) + "  " + info
    else:
        print colorStr[color].format("{0} INFO:".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M")) + "  " + info)

# pyspark 常用官方函数参数 

#DataFrame

#---------------------------------------------------------------------------------------------------------------------------
union(other)
#explain: Return a new DataFrame containing union of rows in this frame and another frame.


#---------------------------------------------------------------------------------------------------------------------------
drop(*cols)
#explain: Returns a new DataFrame that drops the specified column. This is a no-op if schema doesn’t contain the given column name(s).
#eg: df.drop(age) df.drop(df.age)


#---------------------------------------------------------------------------------------------------------------------------
dropDuplicates(subset=None)
#explain: Return a new DataFrame with duplicate rows removed optionally only considering certain columns.
#eg: df.dropDuplicates() df.dropDuplicates([name height])


#---------------------------------------------------------------------------------------------------------------------------
join(other on=None how=None)
#explain:
#Joins with another DataFrame using the given join expression.
#
#Parameters: 
#other – Right side of the join
#on – a string for the join column name a list of column names a join expression (Column) or a list of Columns. If on is a string or a list of strings indicating the name of the join column(s) the column(s) must exist on both sides and this performs an equi-join.
#how – str default ‘inner’. One of inner outer left_outer right_outer leftsemi.
#eg: 
df.join(df2 df.name == df2.name outer).select(df.name df2.height)
#
df.join(df2 name outer).select(name height)
#
cond = [df.name == df3.name df.age == df3.age]
df.join(df3 cond outer).select(df.name df3.age)
#
df.join(df2 name).select(df.name df2.height)
#
df.join(df4 [name age]).select(df.name df.age)

#---------------------------------------------------------------------------------------------------------------------------
filter(condition)
# where() is an alias for filter()
#eg:
df.filter(df.age > 3)
df.where(df.age == 2)

#---------------------------------------------------------------------------------------------------------------------------
 select(*cols)
# Projects a set of expressions and returns a new DataFrame.
# Parameters: cols – list of column names (string) or expressions (Column). If one of the column names is ‘*’ that column is expanded to include all columns in the current DataFrame.
# eg:
# >>> df.select(*).collect()
# >>> df.select(name age)
# >>> df.select(df.name (df.age + 10).alias(age))

#---------------------------------------------------------------------------------------------------------------------------
# pyspark.sql.DataFrameWriter(DataFrame).csv
# DataFrame Save as csv
# explain csv(path mode=None compression=None sep=None quote=None escape=None header=None nullValue=None escapeQuotes=None quoteAll=None dateFormat=None timestampFormat=None)
# df.write.csv("hdfs://user/songziheng/xxx.csv" mode=overwrite header=True)

# pyspark.sql.DataFrameWriter(DataFrame).saveAsTable("caijng_dmp_cdw.xxxxtable" mode=overwrite partitionBy=date) # 按照对应的列插入对应的分区


#---------------------------------------------------------------------------------------------------------------------------
# pyspark.sql.DataFrameReader(spark)
# read DataFrame As csv
# df = spark.read.csv("hdfs://user/songziheng/xxx.csv" sep="\t" header=True inferSchema=True)

#---------------------------------------------------------------------------------------------------------------------------
# UDF udf example
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def func(col):
    if col is None:
        return "NULL".lower()
    lis = dict([tuple(i.split("=")) for i in col.split("&")])
    return lis.get('gender', "NULL").lower()

# 生成udf对象 并写明返回值在spark对应的类型     
parser_gener = udf(func, StringType())
gdf = df.withColumn("gender", parser_gener(df['dp_meta']))  

# 使用指定的schema创建pyspark DataFrame
schema = StructType([StructField('name', StringType()), StructField('age',IntegerType())])
rows = [Row(name='Severin', age=33)]
df = spark.createDataFrame(rows, schema) # 创建非空的DataFrame
df = spark.createDataFrame([], schema) # 创建一个空的DataFrame ch


