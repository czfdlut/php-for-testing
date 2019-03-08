# -*- coding:utf-8 -*-
import redis
import sys
import configparser
import time
import redis_lock

class Singleton(object):
    #python3 is different for object.new
    def __new__(cls, config_path, keyword, logger, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls)
        return cls._instance

class RedisClient(Singleton):
    def __init__(self, config_path, keyword, logger):
        self.logger = logger
        self.pool = None
        self.r_con = None

        try:
            config = configparser.RawConfigParser()
            config.read(config_path)
            timeout = config.getint(keyword, "timeout")
            host = config.get(keyword, "host")
            port = config.getint(keyword, "port")
            passwd = config.get(keyword, "passwd")
            db = config.getint(keyword, "db")
            self.max_retry = config.getint(keyword, "max_retry")
        except Exception as err:
            raise Exception(err)

        self.pool = redis.ConnectionPool(host=host,
                                        port=port,
                                        db=db,
                                        password=passwd,
                                        socket_timeout=timeout)

    def connect(self):
        connection = None
        for try_count in range(self.max_retry):
            try:
                self.r_con = redis.StrictRedis(connection_pool=self.pool)
                connection = self.pool.get_connection("ping")
                break
            except:
                self.logger.warning("ConnectionError:")
                continue

        if connection is None:
            self.logger.error("connection redis failed!")
            return None

        self.logger.info("redis connect is ok!")

        return connection

    def retry_connect(self, redis_client, keyword="REDIS"):
        is_probe_avail = False
        if not self.r_con:
            return self.connect(keyword=keyword)

        for count in range(3):
            if self.r_con.ping():
                is_probe_avail = True
                break
        if not is_probe_avail:
            try:
                self.pool.release(self.r_con)
            except:
                pass
        if is_probe_avail:
            return redis_client
        else:
            return self.connect(keyword=keyword)

    def acquire(self, lock_key, expire):
        lock = redis_lock.Lock(self.r_con, lock_key, expire=expire)
        try:
            if lock.acquire():
                return lock
        except Exception as err:
            self.logger.error(str(err))
        return None

    def release(self, lock):
        if lock:
            lock.release()

    def disconnect(self):
        self.r_con.ping()
        #self.pool.release(self.r_con)
        self.pool.disconnect()

    def sadd(self, key, values):
        if key is None or values is None:
            raise Exception("sadd empty")
        try:
            if len(values) > 0:
                self.r_con.sadd(key, values)
        except Exception as err:
            self.logger.error(err)
            return False
        return True

    def sismember(self, key, member):
        try:
            return self.r_con.sismember(key, member)
        except Exception as err:
            self.logger.error(err)
            return 0

    def smembers(self, key):
        try:
            return self.r_con.smembers(key)
        except Exception as err:
            self.logger.error(err)
            return []

    def hset(self, key, filed, value):
        if key is None or filed is None or value is None:
            raise Exception("hset empty")

        try:
            self.r_con.hset(key, filed, value)
        except Exception as err:
            self.logger.error(err)
            return False
        return True

    def hkeys(self, key):
        try:
            return  self.r_con.hkeys(key)
        except Exception as err:
            self.logger.error(err)
            return []

    def hget(self, key, value):
        try:
            return self.r_con.hget(key, value)
        except Exception as err:
            self.logger.error(err)
            return []

    def hdel(self, key, value):
        try:
            return self.r_con.hdel(key, value)
        except Exception as err:
            self.logger.error(err)
            return []

    def delete(self, names):
        try:
            self.logger.info("redis delete names : %s"%(str(names)))
            if self.r_con.delete(names) == 0:
                self.logger.warning("redis delete not find record")
                return False
            return True
        except Exception as err:
            self.logger.error(err)
            return False

    def srem(self, key, member):
        try:
            self.r_con.srem(key, member)
            self.logger.info("srem:  %s %s"%(key, member))
        except Exception as err:
            self.logger.error(err)
            sys.exit(0)
            return False

        return True

    def lpush(self, key, value):
        try:
            self.r_con.lpush(key, value)
        except Exception as err:
            self.logger.error(err)
            return False

        return True

    def lpop(self, key):
        try:
            lpop_value = self.r_con.lpop(key)
            return lpop_value
        except Exception as err:
            self.logger.error(err)
            return None

    def rpop(self, key):
        try:
            rpop_value = self.r_con.rpop(key)
            return rpop_value
        except Exception as err:
            self.logger.error(err)
            return None

    def get(self, key):
        try:
            return self.r_con.get(key)
        except Exception as err:
            self.logger.error(err)
            return None

    def incrbyfloat(self, key, value):
        try:
            return self.r_con.incrbyfloat(key, value)
        except Exception as err:
            self.logger.error(err)
            return None

    def llen(self, key):
        try:
            llen = self.r_con.llen(key)
            return llen
        except Exception as err:
            self.logger.error(err)
            return 0

    def sinter(self, group1, group2):
        try:
            return list(self.r_con.sinter(group1, group2))
        except Exception as err:
            self.logger.error(err)
            return None

    def sdiff(self, group1, group2):
        try:
            return list(self.r_con.sdiff(group1, group2))
        except Exception as err:
            self.logger.error(err)
            return None

    def sdiffstore(self, source, dest):
        try:
            return self.r_con.sdiffstore(dest, source, dest)
        except Exception as err:
            self.logger.error(err)
            return 0


if __name__ == '__main__':
    from util import logger_handler
    redis_client = RedisClient("./conf/config_test/conf", keyword, logger_handler("test"))
    redis_client.connect()
    #print("111: ", redis_client.hset("msg_host", "aa", "bb"))
    lock = redis_client.acquire("test", 5)
    print("get lock====================", lock)
    #redis_client.release(lock)
