--设置hive运行队列
SET mapreduce.job.queuename=root.caijing.stats;

-- 创建表
--hive 默认的字段分隔符为ascii码的控制符\001,建表的时候用fields terminated by '\001'
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
from test.labeled_user_profile LATERAL VIEW explode(explode_col) table_alias AS origin_id

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

--字符串join
concat_ws('_', cast(uid as string), cast(ut as string))
-- hive常用函数大全
-- https://www.cnblogs.com/MOBIN/p/5618747.html

IF(Test Condition, True Value, False Value)

--获取第一个非null值 适合多个 outer join的场景
COALESCE(value1,value2,...) --该函数用来获取参数列表中的首个非空值，若均为NULL，则返回NULL，例如：

CASE WHEN 

eg:
    select pd,
    case pst
        when "常年" then 1 
        when "非常年" then 0
        else 0
    end
    as pt
    from dgp limit 100;

    select pd,
    case
        when pst＝"常年" then 1 
        when pst＝"非常年" then 0
        else 0
    end
    as pt

--常用统计函数模板
histogram_numeric
rank
row_number
ntile 

--开窗函数模板 
select 
    id, 
    name,
    score,
    row_number() over(partition by name order by score desc) as rk_col,
    row_number() over(partition by score order by name) as row_col, --以最后的分组方式排序输出
from test.rank_test;

--创建桶表 关于桶的操作这一句一定要加
set hive.enforce.bucketing = true;
--按照 author_id 做哈希
create table if not exists caijing_dmp_cdw.zhihu_test_authorinfo (
    author_id            string,
    is_good_author       bigint,
    followers_amount    bigint,
    is_good_answer      string
)
CLUSTERED BY (author_id) INTO 4 BUCKETS;

--桶表抽样
--TABLESAMPLE (BUCKET x OUT OF y [ON colname])
--抽取1/4
select
     author_id,
     is_good_author,
     followers_amount
from caijing_dmp_cdw.zhihu_test_authorinfo TABLESAMPLE(BUCKET 1 OUT OF 4 ON rand()) s
limit 10;
--在表按照author_id分桶的情况下 这样直接回取对应分桶的part 效率高
--from caijing_dmp_cdw.zhihu_test_authorinfo  TABLESAMPLE(BUCKET 1 OUT OF 4 ON author_id) s; 

--分块抽样 保证至少0.1% 至少块大小的数据被返回 所以不会正好是0.1% 
SELECT count(*)
FROM caijing_dmp_cdw.zhihu_test_authorinfo TABLESAMPLE(0.1 PERCENT) s;

--按照数据量抽样 至少100M 但是块大小是256M的话会返回256M
SELECT 
    count(*)
FROM caijing_dmp_cdw.zhihu_test_authorinfo TABLESAMPLE(10M) s;

--输出值可能不是10 
--这种方式可以根据行数来取样，但要特别注意：
--这里指定的行数，是在每个InputSplit中取样的行数，也就是，每个Map中都取样n ROWS。
SELECT count(*) FROM caijing_dmp_cdw.zhihu_test_authorinfo TABLESAMPLE(10 ROWS);

--hive 处理json相关函数
select
    --event 是一个json 字段 
    get_json_object(event, "$.key1"), --获取 json 对象中 key1 对应的值
    get_json_object(event, "$.key1.key2") --获取 深层次中的key的对应的值
    get_json_object(event, "$.key1.key2[0]") --获取数组的内容
from xxtable

--hive json 和 map的转换 
select
    from_json(json_field) as map_field,
    to_json(map_filed) as json
from xxxtable


--hive 正则表达式匹配
select
     regexp_extract(init_session_info, "gender=(\\w*)", 1) -- 获取init_session_info 中符合pattern的 匹配 
     --1 表示取出第一个括号里面的值
from 

--hive 字符串查找 
select
    instr(string str, string substr) 
    --查找字符串str中子字符串substr出现的位置，如果查找失败将返回0，如果任一参数为Null将返回null，注意位置为从1开始的
from 










