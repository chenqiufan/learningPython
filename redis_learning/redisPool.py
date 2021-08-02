# encoding=utf-8

import redis

pool = redis.ConnectionPool(host="localhost", port=6379, max_connections=10, decode_responses=True)
con_1 = redis.StrictRedis(connection_pool=pool)
con_2 = redis.StrictRedis(connection_pool=pool)
con_3 = redis.StrictRedis(connection_pool=pool)
print(con_1.client_id())
print(con_2.client_id())
print(con_3.client_id())
con_1.close()
con_2.close()
con_3.close()
