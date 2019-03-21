### ![image](https://raw.githubusercontent.com/scaluo/innerquery/master/innerquery/static/images/icon.png) Inner Query 轻量的内部数据查询工具  


#### 主要功能
1. 可以查询多种类型的目标数据库，支持mysql、sqlserver、sqlite...
2. 自定义sql查询,结果可以展示为表格、柱图、饼图、曲线图
3. 自定义查询条件，查询条件可以为输入框和选择项
4. 可以进行简单用户管理，权限分为管理员和普通操作人员

#### 安装
支持python3.5+版本  

$pip install pipenv（已安装pipenv请忽略)  
$pipenv --three  
$pipenv install  
$pipenv shell  
$flask run  

访问localhost:5000  
默认用户名admin，密码admin  

配置查询目标数据库连接  
默认安装访问的查询数据库是otherdata.db,修改innerquery目录下的settings.py文件，指定你需要访问的目标数据库，
在SQLALCHEMY_BINDS节点中配置key为target的节点，连接串参见flask-sqlachemy文档。  

访问mssql数据库  
配置MSSQL_TARGET节点，则查询目标数据库为mssql数据库    
如果要使用mssql数据库，需要安装pymssql  
$pipenv install pymssql  


#### 查询定义
##### “sql内容”示例：   
select name '用户名称',phone '电话' from user where name='{0} and sex={1}'  
其中{0}、{1}表示条件占位符  


#####  "输入条件"示例：  
text|姓名  
select|性别|男:1,女:0  
一行代表一个条件  

*关于展示图形的SQL语句必须满足的条件
必须是两列，第一列是统计项，第二列是统计数据  

页面展示效果  
![image](https://raw.githubusercontent.com/scaluo/innerquery/master/innerquery/static/images/example.png)  


