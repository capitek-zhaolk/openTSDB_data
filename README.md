# openTSDB_data 相关代码

**** 参考
1、HBase单机插入能够实现1W~2W之间的插入速度。调用Http Post在单位时间内（1秒），数据最高写入量为18950点/秒，调用Http Post方法的次数为378次，
Http Post接口每调用100次，需耗时：0.250s


2018/5/22 修改
修改了opentsdb的配置文件。
单线程：
批量插入，json_list 最大数数据长度是78
1秒钟最大写入量为27300点，每秒钟调用Http Post接口的次数为350次，每调用100次接口需耗时0.249秒
HBase在单位时间内能够实现1W~3W之间的插入。
相关日志：172.17.0.178:/home/share/interface/Performance/single_print_info.conf


