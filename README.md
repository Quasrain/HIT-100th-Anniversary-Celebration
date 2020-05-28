# HIT-100th-Anniversary-Celebration
100th Anniversary Celebration of HIT

## 1.框架说明
采用django+uwsgi+uginx  
暂时配置在我个人的服务器上  
搭建过程参照：https://www.cnblogs.com/Ph-one/p/11705799.html  

## 2.主要需求
### 2.1 addComment
评论包含以下内容
- Name
- Tag(院系、入学年级等)
- Comment
- Checked(是否通过审核)
- Year(想要穿越回哪一年)  

返回当前评论数

### 2.2 selectComment
选择100条评论进行展示，逻辑是top5+80条top200+20条随机  
现在支持每十年选择10条

### 2.3 like
根据给定的UID点赞

### 2.3 lottery
抽取最后的幸运参与者

## 3. 使用方法
主要通过url的方式传输数据

### 3.1 addComent
http://39.102.52.243/addComment/Name/Tag/Comment/Year    
其中Name, Tag, Comment, Year字段可根据需要自行替换  
例如 http://39.102.52.243/addComment/QAQ/QwQ/Happy/1920  
返回一个正整数表示UID

### 3.2 selectComment
http://39.102.52.243/selectComment  
无需替换字段  
返回至多100个list，按照Year递减的顺序排列  
每个list由如下字段组成：  
[UID, Name, Tag, Comment, Year]

### 3.3 like
http://39.102.52.243/like/UID  
UID字段可根据需要自行替换  
返回点赞后当前UID对应评论的like数

### 3.4 lottery
http://39.102.52.243/lottery  
无需替换字段

返回一个list，格式如下：  
[UID, Name, Tag, Comment, count]（count表示like数）