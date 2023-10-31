## 以User为核心的操作：

### 用户

#### 用户注册

#### 用户登陆

### 番组

#### 创建番组

```python
BangumiInsert(APIView)
请求字段：
request = {
	bangumi_id : ...,
	bangumi_name : ...,
	bangumi_intro : ...
}
# 番组的评分和排名需要在用户评分后进行，因此这两个属性是可空的。
```

#### 更新番组信息

```python
BangumiUpdate(APIView)
请求字段：
request = {
	bangumi_id : ...,
	bangumi_name : ...,
	bangumi_intro : ...
}
# 和前面的创建大同小异
```

#### 删除番组信息

```python
BangumiDelete(APIView)
请求字段：
request = {
	bangumi_id : ...
}
```

### 评分

在评分进行修改之后理应对番组的评分、排名进行修改

#### 新建评分

```python
ScoreInsert(APIView)
请求字段：
request = {
	user_id : ...,
    bangumi_id : ...,
  	score : ...
}
```



#### 更新评分

```python
ScoreInsert(APIView)
请求字段：
request = {
	user_id : ...,
    bangumi_id : ...,
  	score : ...
}
```



#### 删除评分

```python
ScoreInsert(APIView)
请求字段：
request = {
	user_id : ...,
    bangumi_id : ...
}
```



### 发表日志

#### 新建日志

```python
BlogInsert(APIView)
请求字段
request = {
	blog_id : ...,
	title : ...,
	content : ...,
	time : ...,
	
	user_id : ...,
}
```

#### 删除日志

```python
BlogDelete(APIView)
请求字段
request = {
	blog_id : ...
}
```

#### 关联番组

```python
RelateBangumi(APIView)
请求字段
request = {
	blog_id : ...,
	bangumi_id :...
}
# 为什么不把bangumi_id直接当成blog的一个字段呢：因为大多数时候一个日志可能涉及多个番组，因此理论上日志和番组是一对多的关系。
```

#### 删除关联

```python
RelateDelete(APIView)
请求字段
request = {
	blog_id : ...,
	bangumi_id :...
}
# 一次只可以删除一个关联。
```



### 发表评论

#### 新建评论

#### 删除评论