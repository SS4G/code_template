
--answer_infos.txt
drop table caijing_dmp_cdw.zhihu_online_answer_info;
drop table caijing_dmp_cdw.zhihu_online_user_info;
drop table caijing_dmp_cdw.zhihu_online_author_infos;
drop table caijing_dmp_cdw.zhihu_online_question_infos;
drop table caijing_dmp_cdw.zhihu_online_topic_info;
drop table caijing_dmp_cdw.zhihu_online_candidate;
drop table caijing_dmp_cdw.zhihu_online_question_id_dict;
drop table caijing_dmp_cdw.zhihu_online_answer_id_dict;
drop table caijing_dmp_cdw.zhihu_online_test_set;

LOAD DATA LOCAL INPATH '/data00/home/songziheng/private_workspace/zhihu_ccir/online_test/data/candidate_online_20180725.txt'
OVERWRITE INTO TABLE caijing_dmp_cdw.zhihu_online_candidate PARTITION (date='20180725');
LOAD DATA LOCAL INPATH '/data00/home/songziheng/private_workspace/zhihu_ccir/online_test/data/candidate_online_20180726.txt'
OVERWRITE INTO TABLE caijing_dmp_cdw.zhihu_online_candidate PARTITION (date='20180726');
LOAD DATA LOCAL INPATH '/data00/home/songziheng/private_workspace/zhihu_ccir/online_test/data/candidate_online_20180727.txt'
OVERWRITE INTO TABLE caijing_dmp_cdw.zhihu_online_candidate PARTITION (date='20180727');
LOAD DATA LOCAL INPATH '/data00/home/songziheng/private_workspace/zhihu_ccir/online_test/data/candidate_online_20180728.txt'
OVERWRITE INTO TABLE caijing_dmp_cadw.zhihu_online_candidate PARTITION (date='20180728');

select 
    count(*)
from caijing_dmp_cdw.zhihu_answer_infos t0 join 
(select
     answer_id
from caijing_dmp_cdw.zhihu_online_answer_info where date between '20180725' and '20180728') t1 on (t0.answer_id = t1.answer_id) join
(select
    distinct candidate_id as dis_canid
from caijing_dmp_cdw.zhihu_online_candidate where date between '20180725' and '20180728') t3 on (t0.answer_id=t3.dis_canid);

select
     count(answer_id)
from caijing_dmp_cdw.zhihu_online_answer_info where date between '20180725' and '20180728';

 select
    count(*)
from caijing_dmp_cdw.zhihu_answer_infos