# jobplus6-11

LouPlus Team 11 https://www.shiyanlou.com/louplus/python

## Contributors

* [LouPlus](https://github.com/LouPlus)
* [南雁](https://github.com/nanyan375)
* [爱喝茶](https://github.com/teawithme)
* [王小六](https://github.com/wkandking)

## 项目说明

本项目是用于练习python+flask的一个在线招聘网站。web框架使用flask，数据库使用mysql，前端套用bootstrap。主要实现的功能如下：

* 用户的注册，登录
* 管理员的后台管理
* 企业列表的展示
* 职位列表的展示
* 企业职位发布与投递管理
* 求职者的简历投递

目前还有更多功能尚在完善中...

## 环境配置

首先，将代码克隆到本地：

`$ git clone http://github.com/LouPlus/jobplus6-11`

进入jobplus6-11目录后，可在本地生成一个虚拟环境（需安装`virtualenv`），命名为`env`：

`$ virtualenv env`

然后，激活虚拟环境

`$ source env/bin/activate`

在虚拟环境里安装项目所需的依赖包

`(env)$ sudo pip install -r requirements.txt`

## 运行项目

创建数据库
```
(env)$ sudo service mysql start
(env)$ mysql -uroot
> create database jobplus;
> exit
```
设置环境变量
```
(env)$ export FLASK_APP=manage.py
(env)$ export FLASK_DEBUG=1
```
将测试数据写入数据库
```
(env)$ flask shell
>>> from scripts.generate_test_datas import run
>>> run()
>>> exit
```
运行项目

`(env)$ flask run`

## 数据库的管理
在对表格进行数据更改时可以使用flask-migrate来进行数据库管理
```
(env)$ flask db init
(env)$ flask db migrate -m 'init the database'
(env)$ flask db upgrade
```

## 测试账户

数据库里已经写入了测试所需的各类账户

类型 | 帐号 | 密码
:-|:-:|:-:
管理员 | admin@example.com | jobplus
普通用户 | jackma@example.com | jobplus
企业用户 | abc@example.com | jobplus

