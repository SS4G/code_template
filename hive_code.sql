--设置hive运行队列
SET mapreduce.job.queuename=root.caijing.stats;

-- 创建表
create table if not exists caijing_dmp_stats.aweme_latest30days_active_dates_daily(
    user_id bigint,
    nf_fans_delta array<string>,
    active_days bigint,
    latest_active_date date
)
row format delimited
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
PARTITIONED BY(`date` STRING) STORED AS PARQUET;


--create table if not exists test.table as --根据结果直接创建表
--INSERT OVERWRITE TABLE caijing_dmp_stats.aweme_latest30days_active_dates_daily PARTITION(date='${hivevar:current_date}')  插入分区 
-- 结果插入本地目录
insert overwrite local directory '/data00/home/songziheng/workspace2/jiangkangwenda/user_kws_with_label'
row format delimited
FIELDS TERMINATED BY '\t'
COLLECTION ITEMS TERMINATED BY ','
MAP KEYS TERMINATED BY ':'
select
    uid, 
    ut, 
    gender,
    age,
    label,
    kws
from test.user_kws; 

--行转列
select
    uid,
    ut, 
    origin_id
from test.labeled_user_profile LATERAL VIEW explode({0}) user_profile_list AS origin_id

--删除表
drop table caijing_dmp_stats.aweme_latest30days_active_dates_dailyxxxx;

--重命名表
ALTER TABLE $table_name RENAME TO $new_table_name;

--重命名列
ALTER TABLE table_name CHANGE $col_old_name $col_new_name $column_type


--删除表的某个分区
ALTER TABLE test.test_behavior_adclick_month_full DROP IF EXISTS PARTITION (month='201802')

--向表中load数据 需要在创建表的时候指定各个级别的分隔符
LOAD DATA LOCAL INPATH '/data00/home/songziheng/jiaojiulong_loan_table/error_code_map.txt' OVERWRITE INTO TABLE test.bank_errorcode_errorreason_map;

--时间日期转换
--unix_timestamp(date, 'yyyyMMdd')  日期或者时间转换为时间戳
--from_unixtime($timestamp, 'yyyy-MM-dd') 时间戳转换为对应格式时间的字符串
--常用转换
from_unixtime(unix_timestamp(date, 'yyyyMMdd'), 'yyyy-MM-dd')

--子串  substr(str, st) st 从1 开始 表示从st之后的所有字符
--子串  substr(str, st，offset) st 从1 开始 offset 长度 表示从st之后的所有字符

substr("abcdefgh", 2) as doc_short_id,     --return 'bcdefgh'
substr("abcdefgh", 2, 3) as doc_short_id,  --return 'bcd'

--切分字符串 
--split(str, regex) -- 注意一定要是合法的正则表达式 | \ 这类字符 都要做转义  如 | 转义为 \\|
split('aaa|bbb|ccc', "\\|")


--类型转换 
--cast(col as type)
cast('123' as bigint)

-- hive常用函数大全
-- https://www.cnblogs.com/MOBIN/p/5618747.html







