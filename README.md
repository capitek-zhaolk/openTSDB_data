# openTSDB_data 相关代码

**** 参考
1、HBase单机插入能够实现1W~2W之间的插入速度。调用Http Post在单位时间内（1秒），数据最高写入量为18950点/秒，调用Http Post方法的次数为378次，
Http Post接口每调用100次，需耗时：0.250s


2018/5/22 修改
修改了opentsdb的配置文件。
单线程：
批量插入，json_list 最大数数据长度是73
1秒钟最大写入量为 2.3W+ 点，每秒钟调用Http Post接口的次数为319次，每调用100次接口需耗时0.267秒
HBase在单位时间内能够实现1W~3W之间的插入。
单个线程处理1W条数据，耗时0.429s

相关日志：172.17.0.178:/home/share/interface/Performance/single_print_info.conf



2018/5/13 修改
多线程
由于单线程的因素
在使用多线程、批量往数据库插入数据时，需要把批量数做一下均分。相关codes：

'''
# 线程数(没加锁)
thread_nums = 10
# json_list批量插入数据长度
lists_nums_ = 66
total_nums = 100000
'''
每个线程每秒钟最大的写入量为 2.2W+ 条，每秒钟调用Http Post接口的次数为 346+ 次，每调用100次接口需耗时0.245秒.
HBase在单位时间内能够实现 2.2W+ 的插入。
相关日志：172.17.0.178:/home/share/interface/Performance/multi_print_info.conf

10个线程处理10W条数据，耗时43.725s，平均每个线程处理10W条数据，条耗时4.372s

相关日志：172.17.0.178:/home/share/interface/Performance/multi_print_info.conf


'''
# 线程数(加锁)
thread_nums = 10
# json_list批量插入数据长度
lists_nums_ = 66
total_nums = 100000
'''
每个线程每秒最大写入量为 1.7W+ 条，每秒钟调用Http Post接口的次数为 265+ 次，每调用100次接口需耗时0.3秒.
平均响应时间为0.0003s
HBase在单位时间内能够实现 1.7W+ 的插入。

10个线程处理10W条数据，耗时5.710s，平均每个线程处理1W条数据，耗时0.571s


相关日志：172.17.0.178:/home/share/interface/Performance/multi_lock_print_info.conf














