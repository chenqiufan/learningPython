"""
使用dbutils创建连接Mysql的线程池
"""
import pymysql
from dbutils.pooled_db import PooledDB


"""
创建mysql线程池：
    creator:pymysql 使用连接数据库有的模块
    maxconnections: 连接池允许的最大连接数，0/None表示无限制
    maxcached： 连接池中最多闲置的连接，0/None表示无限制
    mincached：初始化时，连接池中至少创建的空闲的连接，0表示不创建
    maxshared：连接池中最多共享的连接数量，无用，因为pymsql的连接就是共享的
    blocking：如果没有可用连接时是否阻塞等待。True:等待；False：不等待并且报错
    maxusage：一个连接最多可以被重复使用的次数，None表示无限制
    setsession：开始会话前执行的命令列表。如"set datastyle to ..."
    ping: 0=None=never
          1=default=whenever it is required
          2=when a cursor is created
          4=when a query is executed
          7=always  
"""
pool = PooledDB(
    creator=pymysql,
    maxusage=2,
    setsession=[],
    ping=1,
    maxcached=5,
    mincached=2,
    maxshared=3,
    host="localhost",
    user="root",
    password="123456",
    database="demo",
    charset="utf8"
)

def func():
    """
    首先检测当前正在运行的连接数是否小于最大连接数，如果小于，等待或报错
    会优先去初始化时创建的连接中获取连接 steadyDBConnection
    然后将SteadyDBConnection对象封装到PooledDedicatedDBConnection中并返回
    如果最开始创建的链接没有链接，则去创建一个SteadyDBConnection对象，再封装到PooledDedicatedDBConnection中并返回
    一旦关闭链接后，连接就返回到连接池让后续线程继续使用
    :return:
    """
    conn = pool.connection(shareable=False)
    cursor = conn.cursor()
    cursor.execute("select * from users")
    result = cursor.fetchall()
    print(result)
    conn.close()
func()
