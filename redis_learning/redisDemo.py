# encoding=utf-8

from redis import StrictRedis

# 创建连接, decode_responses=True返回的是字符串，不然返回的是byte
try:
    con = StrictRedis(host="localhost", port=6379, db=1, decode_responses=True)
except Exception as e:
    print(e)

con.set("name", "zhu jian")
res = con.get("name")
print(res)
con.delete("name")
con.close()
