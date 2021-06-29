"""
通过Pymsql操作mysql

pip3 install pymysql

CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
AUTO_INCREMENT=1 ;
"""

import pymysql

"""
创建mysql连接：
    cursorclass：定义返回结果的数据结构
"""
conn = pymysql.connect(host="localhost",port=3306,user="root",password="123456",charset="utf8",db="demo",cursorclass=pymysql.cursors.DictCursor)

# 插入
try:
    # Cursor类自动实现了__enter__ 和 __exit__方法
    with conn.cursor() as cursor:
        sql = "insert into users(username,password) values('admin','123456')"
        cursor.execute(sql)
        conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()

# 查找
try:
    with conn.cursor() as cursor:
        sql = "select * from users"
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        """
        [{'id': 1, 'username': 'admin', 'password': '123456'}]
        """
except Exception as e:
    print(e)
finally:
    conn.close()

# 更新
try:
    with conn.cursor() as cursor:
        sql = "update users set username='test' where id = 1"
        cursor.execute(sql)
        conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()

# 删除
try:
    with conn.cursor() as cursor:
        sql = "delete from users where username='test'"
        cursor.execute(sql)
        conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    conn.close()