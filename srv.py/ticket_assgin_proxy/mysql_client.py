# -*- coding: utf-8 -*
from util import logger_handler
import configparser
import mysql.connector
import mysql.connector.pooling
from mysql.connector import errorcode

class MySqlClient(object):
    def __init__(self, config_path, keyword, logger):
        self.logger = logger
        self.dbconfig = None
        self.cnxpool = None

        try:
            config = configparser.RawConfigParser()
            config.read(config_path)
            self.dbconfig = {
                'user': config.get(keyword, "user"),
                'password': config.get(keyword, "password"),
                'host': config.get(keyword, "host"),
                'port': config.getint(keyword, "port"),
                'database': config.get(keyword, "database")
                }
            self.pool_name = config.get(keyword, "pool_name")
            self.pool_size = config.getint(keyword, "pool_size")
        except Exception as e:
            raise Exception(str(e))
            sys.exit()

    def connect(self):
        try:
            self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(
                                                        pool_name=self.pool_name,
                                                        pool_size=self.pool_size,
                                                        pool_reset_session=True,
                                                        **self.dbconfig)
        except mysql.connector.Error as err:
            self.logger.error("mysql connect error %s" % err)
            return err
        except Exception as err:
            self.logger.error("mysql connect error %s" % err)
            return err
        return None

    def execute_query_sql(self, sql):
        cnx = None
        cursor = None
        results = None

        try:
            cnx = self.cnxpool.get_connection()
            cnx.set_charset_collation('utf8')

            cursor = cnx.cursor()
            cursor.execute(sql)

            results = cursor.fetchall()
        except mysql.connector.Error as err:
            self.logger.error("mysql connect error %s %s"%(str(err), sql))
        except Exception as err:
            self.logger.error("query result error: %s %s"%(str(err), sql))
        finally:
            if cursor:
                cursor.close()
        if cnx:
            cnx.close()
        return results

    def insert(self, table, hdata):
        cnx = None
        cursor = None

        try:
            cnx = self.cnxpool.get_connection()

            cnx.set_charset_collation('utf8')
            cursor = cnx.cursor()

            bdata  = tuple(hdata.values())
            fields = tuple(hdata.keys())

            sql = "INSERT INTO %s %s VALUES ("%(table, fields)
            sql  = sql.replace("'", "`")
            sql = sql + ("%s,"*len(fields))[:-1] + ")"

            cursor.execute(sql, bdata)
            cnx.commit()
        except mysql.connector.Error as err:
            self.logger.error("mysql connect error %s %s"%(str(err), sql))
            return err
        except Exception as err:
            self.logger.error("query result error: %s %s"%(str(err), sql))
            return err
        finally:
            if cursor:
                cursor.close()
        if cnx:
            cnx.close()

        return None

    def init_memlock(self, table, uid):
        qs = self.execute_query_sql("select uid from '%s' where uid='%s'" % (table, uid))
        if qs is not None or len(qs) > 0:
            return True

        ret = self.insert(table, {"uid": uid, "status": 1})
        if ret is not None:
            return False

        return True

    def acquire(self, table, uid):
        pass

    def release(self, table, uid):
        pass

    def batch_insert(self, table, hdatas):
        cnx = None
        cursor = None

        try:
            cnx = self.cnxpool.get_connection()

            cnx.set_charset_collation('utf8')
            cursor = cnx.cursor()

            bdatas  = [tuple(data.values()) for data in hdatas]
            fields = tuple(hdatas[0].keys())

            sql = "INSERT INTO %s %s VALUES ("%(table, fields)
            sql  = sql.replace("'", "`")
            sql = sql + ("%s,"*len(fields))[:-1] + ")"

            cursor.executemany(sql, bdatas)
            cnx.commit()
        except mysql.connector.Error as err:
            self.logger.error("mysql connect error %s %s"%(str(err), sql))
            return err
        except Exception as err:
            self.logger.error("query result error: %s %s"%(str(err), sql))
            return err
        finally:
            if cursor:
                cursor.close()
        if cnx:
            cnx.close()

        return None

    def execute_sql(self, sql):
        cnx = None
        cursor = None
        try:
            cnx = self.cnxpool.get_connection()

            cnx.set_charset_collation('utf8')
            cursor = cnx.cursor()
            cursor.execute(sql)

            cnx.commit()
        except mysql.connector.Error as err:
            self.logger.error("mysql connect error %s %s"%(str(err), sql))
            return err
        except Exception as err:
            self.logger.error("sql error: %s %s"%(str(e), sql))
            return err
        finally:
            if cursor:
                cursor.close()
        if cnx:
            cnx.close()

        return  None

if __name__ == "__main__":
    obj = MySqlClient("./conf/config_test.conf", "MYSQL", logger_handler("test"))
    obj.connect()
    result = obj.execute_query_sql("select order_ticket.id from order_ticket, account_balance where order_ticket.uid='for_test' and account_balance.balance>1.0 limit 1")
    print("result: ", result)

    hdata = {'uid': 'for_test', 'status': 1, "orderNo": "orderNo", 'merchantCode': '00001', 'merchantName': '携程订票系统', 'bizNo': '10000123', 'bizName': '订票', 'orderDate': '2018-09-01', 'ticketPrices': '368.5', 'mobile': '13800138000', 'requestID': '20180606000005', 'updateTime': '2019-03-01 18:35:30'}
    obj.insert("order_ticket", hdata)

    # hdatas = [
    #     {
    #         "uid": "22",
    #         "merchantCode": "code",
    #         "merchantName": "mame",
    #         "bizNo": "bizNo",
    #         "bizName": "bizName",
    #         "bizTime": "2019-02-25 11:15:00",
    #         "orderNo": "orderNo",
    #         "ticketPrices": 34.5,
    #         "data": "aaaa"
    #     }
    # ]
    # #obj.batch_insert("order_ticket", hdatas)
    # obj.insert("order_ticket", hdatas[0])
    # print("query: ", obj.execute_query_sql("select * from order_ticket"))
    #
    # sql = "select id from order_ticket where uid='22' limit 1"
    # print("query result====: ", obj.execute_query_sql(sql))
