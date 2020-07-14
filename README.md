# ShowBackup

#### 介绍
`showbackup`是一个短小精干的MySQL数据库备份脚本，支持全库，指定库，指定表，定时快速备份。
- 支持全库备份，指定库备份，指定表备份
- 支持备份输出sql文件或压缩文件
- 支持定时自动化备份任务
- 支持清理过期历史备份文件


#### 安装
```shell script
$ pip3 install showbackup
```

#### 配置
运行`showbackup --config`来查看配置文件的位置，使用vi编辑它：
```shell
$ showbackup --config
  请通过编辑showbackup配置文件来完成配置
  vi /your/showbackup/path/conf.json
```
配置文件说明
```json
{
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "usr": "root",
    "pwd": "",
    "source": [
        {"db": "testdb01", "tables": ["users", "posts"]},
        {"db": "testdb02"}
    ],
    "backup_path": "./backup",
    "is_zip": false,
    "every_day_at": "17:49",
    "keep_days": "3"
  }
}
```
```javascript
/**
 * host: 表示mysql的连接地址
 * port: mysql的端口号
 * usr: 用于备份数据库的账号
 * pwd: 用于备份数据库的密码
 * source: 备份的数据内容（支持全库备份，指定库备份，指定表备份）
    - 全库备份
      source: []
 
    - 指定库，eg.备份testdb01和testdb02两个数据库
      source: [{'db':'testdb01'}, {'db': 'testdb02'}] 

    - 指定表，eg.备份testdb01数据库和仅备份testdb02中的users和posts表
      source: [
          {'db':'testdb01'}, 
          {'db': 'testdb02', 'tables':['users', 'posts']}
      ]
 * backup_path: 填写备份文件存放的目录，比如 /backup/mysql
 * is_zip: 是否启用压缩
 * every_day_at: 
    - 每天执行备份的时间点，支持HH:MM:SS 或者 HH:MM
    - eg. 每天凌晨三点整，03:00
    - eg. 每天凌晨三点零八分二十六秒，03:08:26
 * keep_days: 历史备份文件保留最近几天
 */
```

#### 使用
手动执行
```shell script
# 手动执行一次数据库备份，备份完成程序自动退出
$ showbackup mysql
  所有任务均已完成，总耗时12.32秒

$ tree /backup/mysql
  mysql
  └── 201800712_135955
      ├── testdb02
      │   ├── table_user.sql.gz
      │   └── table_visitor.sql.gz
      └── test_len
          └── db_test_len.sql.gz 

```

后台运行
```shell script
# 开始一个数据库定时备份的后台任务
$ showbackup mysql -s &
  将于每天 03:00 开始执行备份任务...

# 结束后台任务（找出showbackup的PID，杀掉PID）
$ ps -ef | grep showbackup
  25415 16958 0 1:35PM ttys001 0:00.24 /usr/bin/python /usr/bin/showbackup mysql -s
$ kill -9 25415
```

使用supervisor运行
```editorconfig
# supervisor配置文件
[program:showbackup]
command=/your/showbackup/path/bin/showbackup mysql -s ; 程序启动命令
```
```shell script
$ supervisorctl
  showbackup STOPED
  supervisor> start showbackup
  supervisor> status
  showbackup RUNNING pid 18245, uptime 0 days, 0:0:03
```



