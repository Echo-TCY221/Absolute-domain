# Absolute domain

##### 运行环境：

python3.0以上

mongodb数据库

python库：

re、json、datetime、time、requests、random、lxml、pymongo、os

`pip install requests`

`pip install lxml`

`pip install pymongo`

##### 使用流程：

首先运行initializer.py初始化程序，创建数据表Category_list --> 运行main.py程序.![image-20230811165109511](C:\Users\tang\AppData\Roaming\Typora\typora-user-images\image-20230811165109511.png)

字段参考mongodb --> py_db --> Category_list中的 list_name 字段.

![image-20230811165920397](C:\Users\tang\AppData\Roaming\Typora\typora-user-images\111.png)

页码参考网页页码（可冗余）

##### 数据保存位置

data --> 图片

version --> 123.json

###### 表结构：

![image-20230811172720830](C:\Users\tang\AppData\Roaming\Typora\typora-user-images\image-20230811172720830.png)



