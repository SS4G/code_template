# 基本语法
## 字符串
#字符串截取
# ${string: start :length}    从 string 字符串的左边第 start 个字符开始，向右截取 length 个字符。
# ${string: start}    从 string 字符串的左边第 start 个字符开始截取，直到最后。
# ${string: 0-start :length}  从 string 字符串的右边第 start 个字符开始，向右截取 length 个字符。
# ${string: 0-start}  从 string 字符串的右边第 start 个字符开始截取，直到最后。
# ${string#*chars}    从 string 字符串第一次出现 *chars 的位置开始，截取 *chars 右边的所有字符。
# ${string##*chars}   从 string 字符串最后一次出现 *chars 的位置开始，截取 *chars 右边的所有字符。
# ${string%*chars}    从 string 字符串第一次出现 *chars 的位置开始，截取 *chars 左边的所有字符。
# ${string%%*chars}   从 string 字符串最后一次出现 *chars 的位置开始，截取 *chars 左边的所有字符。

a="abcdefg"
# ${string: start :length}
echo ${a:1:3} # bckd

# 字符串包含判断 
strA="helloworld"
strB="low"
if [[ $strA =~ $strB ]] #
then
    echo "包含"
else
    echo "不包含"
fi

if [[ a > 1 ]];
then
    echo ${a}
fi 

## 条件语句
## 推荐使用 [[  ]] 注意内部的两边都要有空格 
## < > == 比较的是字符串的字典顺序 -gt -lt -ge -eq 才是比较的 数值的 这个要注意
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi

# contition 的形式
condition1

## 数组
# 数组迭代
arr=(a b c)
for i in ${a[@]};
do
    echo ${i}
done

# 数组中某个元素
echo ${arr[1]} # return b 第2个元素 索引从0开始 


# date 获取指定日期 前后的n天 ! 注意 mac系统 不适用
date -d "20151001  1 days ago"  "+%Y%m%d" # 获取 一天前的日期 使用 "+%Y%m%d"指定日期格式
date -d "${src}  ${data_time_out} days ago"  "+%Y%m%d"

grep
format: grep [option] <pattern> 
-i       # 忽略大小写
-o      #只显示匹配内容
-v      # 只显示不匹配的行
-P      # 正则表达式
-l       # 列出包含对应内容的文件名
-L     #  列出不包含对应内容的文件名
-C 5  # 显示匹配行的前后五行
-A 5  # 显示匹配行的后五行
-B 5  # 显示匹配行的前五行

WC
format: wc [option]
-c或--bytes或--chars  #只显示Bytes数。
-l或--lines          #只显示行数。
-w或--words          #只显示字数。

date 
format: date [option] +[format]
-d datestr : 显示 datestr 中所设定的时间 (非系统时间) "-3 hour" 表示3小时前 "+2 days" 表示两天后
-u : 显示目前的格林威治时间 

# 格式含义字符串 
%Y : 完整年份 (0000..9999)
%m : 月份 (01..12)
%d : 日 (01..31)
%H : 小时(00..23)
%M : 分钟(00..59)
%S : 秒(00..61)
%A : 星期几 (Sunday..Saturday)

%D : 直接显示日期 (mm/dd/yy)
%j : 一年中的第几天 (001..366)
%w : 一周中的第几天 (0..6)
%W : 一年中的第几周 (00..53) (以 Monday 为一周的第一天的情形)

eg: date -d "-3 hour" +"%Y%m%d %H"

find 
format: find <target_path> -name <name_pattern>
eg:  find ./src -name *.c  #查找./src 下面后缀为.c 的文件 
eg:  find ./src -name *rr* -type d  #查找./src 下面名称包含rr的文件夹
　　b 块设备文件
　　d 目录
　　c 字符设备文件
　　p 管道文件
　　l 符号链接文件
　　f 普通文件
eg:  cat $(find ./ -name *.py) | wc -l #统计当前目录下

sort
format: sort <file or stdin>
-b 忽略每行前面开始出的空格字符。
-c 检查文件是否已经按照顺序排序。
-d 排序时，处理英文字母、数字及空格字符外，忽略其他的字符。
-f 排序时，将小写字母视为大写字母。
-n 依照数值的大小排序。
-r 以相反的顺序来排序。
-t<分隔字符> 指定排序时所用的栏位分隔字符。

nl 
format: nl [option] file <tar_file.tar> <file or directory> 
-a #包括空白行也加上行号  

tar 
format: tar [option] <tar_file.tar> <file or directory> 
-cvf sysconfig.tar /etc/sysconfig     #打包到tar
-rvf sysconfig.tar /etc/sysconfig/    # 追加到tar
-tvf sysconfig.tar                               # 查看压缩文件内容
-xvf sysconfig.tar [file_in_tar]          # 解压tar文件   [file_in_tar]  可指定tar内具体文件
-czvf sysconfig.tar.gz                       #/etc/sysconfig/
-xzvf sysconfig.tar.gz [file_in_tar]   # 解压的对应tar.gz [file_in_tar]  可指定tar内具体文件

unzip
format:  unzip [-cflptuvz][-agCjLMnoqsVX][-P <密码>][.zip文件][文件][-d <目录>][-x <文件>] 或 unzip [-Z]
-l 显示压缩文件内所包含的文件
-P<密码> 使用zip的密码选项
-d<目录> 指定文件解压缩后所要存储的目录。
-x<文件> 指定不要处理.zip压缩文件中的哪些文件
 
zip
format:  zip [-AcdDfFghjJKlLmoqrSTuvVwXyz$][-b <工作目录>][-ll][-n <字尾字符串>][-t <日期时间>][-<压缩效率>][压缩文件.zip][文件...][-i <范本样式>][-x <范本样式>]
-d 从压缩文件内删除指定的文件
-i<范本样式> 只压缩符合条件的文件。
-r 递归处理，将指定目录下的所有文件和子目录一并处理
-v 显示指令执行过程或显示版本信息。
-u 更换较新的文件到压缩文件内
-P <密码> 

sed

md5sum 
format:   md5sum [OPTION]... [FILE]...
-b或 --binary:以二进制模式读入文件；
-t或 --text:以文本文件模式读入文件（默认）；

awk

top / htop / iotop
top 原生的自带查看进程的命令
htop 带有各个cpu核心的 查看进程命令
iotop 查看磁盘io使用率的命令

cut

split
切分文件 

less / more
可以使用类似于vim的命令直接在终端中进行搜索

uniq 
类似于 cat 但是会删除相同的行

du
查看磁盘使用情况 
du -h --max-depth=5 

ln  
-s  [源文件或目录]  [目标文件或目录]

tee
将标准输入重定向输出到多个文件 说白了就是把标准输入的内容 同时吧内容显示到标准输出上

下面的命令可以吧结果同时输出到多个文件中
ping baidu.com | tee ping.log ping-baidu.log

parallel 
parallel [options] [command [arguments]] (::: arguments|:::: argfile(s))...
更多详见博客 https://www.jianshu.com/p/cc54a72616a1
并行运行多个job
eg:
parallel  -j $JOB --joblog $LOG_FILE --eta ./spark_submmit.sh ${SRC_PATH}/nl_supervised_keywords_stay_tfidf_sqrt.py  {1} ::: `./date_range.sh $START_DATE $END_DATE`

::: 后面的内容会被替换到 {1} 中 （注意::: 前后的空格） 
parallel ./test_p.sh {1} {2} ::: 1 2 3 ::: 4 5 6
会产生如下笛卡尔积的结果  {}
args1=1 args2=4
args1=1 args2=5
args1=1 args2=6
args1=2 args2=4
args1=2 args2=5
args1=2 args2=6
args1=3 args2=4
args1=3 args2=5
args1=3 args2=6

非笛卡尔积的参数填充方式  {1} 参数和 {2} 参数一一对应
parallel --xapply ./test_p.sh {1} {2} ::: 1 2 3 ::: 4 5 6 
结果如下：
args1=1 args2=4
args1=2 args2=5
args1=3 args2=6

:::: argfile(s) 可以把参数按照行写在文件中 （注意:::: 前后的空格） 

shell数组
0 定义 
a=(1 2 3) # 用空格分割

1 获取某个元素 索引从0开始
b=${a[1]}

2 获取可迭代的list
for i in ${a[@]};
do 
     echo $i
done 
可以认为 ${a[@]} 是类似于 $(ls) 的一种list结果 可以作为传入 parallel的参数 

3 获取所有元素
echo ${a[@]}
