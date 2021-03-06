# HIT-100th-Anniversary-Celebration
100th Anniversary Celebration of HIT

## 1.框架说明
采用django+uwsgi+uginx  
暂时配置在我个人的服务器上  
搭建过程参照：https://www.cnblogs.com/Ph-one/p/11705799.html  

## 2.主要需求
### 2.1 addComment
评论包含以下内容
- Department
- Grade
- Identity
- Name
- Comment
其中每个字段都丢进百度文本内容审核。

返回一个json，包含两个字段  
- status: 200表示正常，210表示重复输入， 211表示未通过审核
- UID: 一个正整数表示UID， 如果未通过审核返回-1

### 2.2 selectComment
有两种模式
- 弹幕模式：一次性全部返回
- 分页模式：给定需求的页面，返回对应页的信息

返回一个json，包含三个字段
- status: 200表示成功
- size: 表示当前页的评论数
- data：一个list，包含评论信息
### 2.3 like
给指定UID对应的评论点赞

返回一个json，包含两个字段
- status: 200表示成功
- Count: 表示当前like数

### 2.4 lottery
抽取最后的幸运参与者，可多次抽取
返回一个json
- status: 200表示成功
- data： 获奖信息

## 3. 使用方法
主要通过url的方式传输数据

### 3.1 addComent
http://39.102.52.243/addComment?Department=department&Grade=grade&Identity=identity&Name=name&Post=post&Phone=phone  
其中department, grade, identity, name, post, phone字段可根据需要自行替换  

返回一个正整数表示UID,UID为7位数，从1000000开始

### 3.2 selectComment
http://39.102.52.243/selectComment?Page=x  
x为所请求的页
- x <= 0 表示弹幕模式，返回所有评论
- x > 0 表示返回对应页的评论  

### 3.3 like
http://39.102.52.243/like?UID=uid
uid字段可根据需要自行替换  
返回点赞后当前uid对应评论的like数

### 3.4 lottery
http://39.102.52.243/lottery  
无需替换字段