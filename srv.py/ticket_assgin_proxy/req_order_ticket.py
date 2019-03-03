# -*- coding: utf-8 -*
from util import request_query
import tornado.web
from datetime import datetime
import json
import requests
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient
import tornado.httpclient

class ReqOrderTicket(tornado.web.RequestHandler):
    def initialize(self):
        self.url = self.config.get("REQ-API", "url")
        self.timeout = self.config.getint("REQ-API", "timeout")

    @property
    def logger(self):
        return self.application.logger

    @property
    def mysql_db(self):
        return self.application.mysql_db

    @property
    def redis_client(self):
        return self.application.redis_client

    @property
    def config(self):
        return self.application.config

    def update_balance(self, uid, balance):
        sql = "update account_balance set balance=%f where uid='%s'" % (balance, uid)
        self.mysql_db.execute_sql(sql)

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()

    def content_type_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "content-type":
                return {k: v}
        return {}

    def process_request_balance(self, uid, request_body):
        sql = "select balance from account_balance where uid='%s' limit 1" % uid
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            self.logger.error("not found balance")
            return None

        balance = qs[0][0]

        try:
            param = json.loads(self.get_argument("param"))
            money = param["ticketPrices"]
        except Exception as err:
            self.logger.error("Error: %s" % err)
            return None

        f_balance = float(balance) -  float(money)

        if f_balance < 1.0:
            self.logger.error("balance is not enough: cost:%s balance:%s" % (money, balance))
            return None

        self.logger.info("final balance: %f" % f_balance)
        return f_balance

    def request_parm_check(self):
        try:
            param = json.loads(self.get_argument("param"))
        except Exception as err:
            return "Error: %s" % err

        if "merchantCode" not in param:
            return "Error: not found merchantCode"

        if "bizNo" not in param:
            return "Error: not found bizNo"

        if "bizName" not in param:
            return "Error: not found bizName"

        if "bizTime" not in param:
            return "Error: not found bizTime"

        if "orderDate" not in param:
            return "Error: not found orderDate"

        if "ticketPrices" not in param:
            return "Error: not found ticketPrices"

        if "payType" not in param:
            return "Error: not found payType"

        if "requestID" not in param:
            return "Error: not found requestID"

        return None

    def join_db_data(self, uid, server_resp_data):
        hdata = {"uid": uid}
        try:
            param = json.loads(self.get_argument("param"))
            resp_data = json.loads(server_resp_data)
            try:
                if int(resp_data["errcode"]) != 0:
                    hdata["status"] = 0
                else:
                    hdata["status"] = 1
            except:
                hdata["status"] = 0 
        except Exception as err:
            self.logger.error("Error: %s" % err)
            return None
        
        if "merchantCode" in param:
            hdata["merchantCode"] = param["merchantCode"]

        if "merchantName" in param:
            hdata["merchantName"] = param["merchantName"]

        if "bizNo" in param:
            hdata["bizNo"] = param["bizNo"]

        if "bizName" in param:
            hdata["bizName"] = param["bizName"]

        if "orderDate" in param:
            hdata["orderDate"] = param["orderDate"]

        if "orderNo" in param:
            hdata["orderNo"] = param["orderNo"]

        if "ticketPrices" in param:
            hdata["ticketPrices"] = param["ticketPrices"]

        if "mobile" in param:
            hdata["mobile"] = param["mobile"]

        if "requestID" in param:
            hdata["requestID"] = param["requestID"]

        if "merchantCode" in param:
            hdata["merchantCode"] = param["merchantCode"]

        if "orderTicketFlow" in param:
            hdata["orderTicketFlow"] = param["orderTicketFlow"]

        hdata["updateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return hdata

    def set_response_header(self, headers):
        for k, v in headers.items():
            self.set_header(k, v)

    def set_response_status(self, status):
        self.set_status(status)

    def get_uid_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "ticket-uid":
                return v
        return None
    
    @tornado.gen.coroutine    
    def reqeust_proxy_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=self.timeout)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()

        uid = self.get_uid_from_headers()
        self.logger.info("ticket uid: %s url: %s" % (uid, self.url))

        sql = "select order_ticket.id from order_ticket, account_balance where order_ticket.uid='%s' \
                        and account_balance.balance>1.0 limit 1" % uid

        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            self.finish_err_msg("uid error")
            return

        err = self.request_parm_check()
        if err is not None:
            self.logger.error(err)
            self.finish_err_msg("param exception")
            return

        lock = self.redis_client.acquire(uid + "_lock", 3)

        f_balance = self.process_request_balance(uid, self.request.body)
        if f_balance is None:
            self.redis_client.release(lock)
            self.finish_err_msg("balance error")
            return
         
        headers = self.content_type_from_headers()
        resp_headers, resp_data, err = yield tornado.gen.Task(self.reqeust_proxy_server, headers, self.request.body)

        self.logger.info("resp_headers: %s" % str(resp_headers))
        self.logger.info("resp_data: %s" % str(resp_data))

        if err is not None:         
            self.logger.error("request error:%s" % err)
            self.redis_client.release(lock)
            self.write(err)
            self.finish()
            return
         
        resp_headers = {"Content-Type":"application/json"}
        self.set_response_header(resp_headers)
        self.set_response_status(200)
        
        hdata = self.join_db_data(uid, resp_data)
        print("hdata: ", hdata)

        self.logger.info("hdata: %s" % str(hdata))         
        if hdata is None:
            self.logger.error("db data error")
            self.redis_client.release(lock)
            self.write(resp_data)
            self.finish()
            return
         
        self.mysql_db.insert("order_ticket", hdata)

        self.update_balance(uid, f_balance)

        self.redis_client.hset("ticket-uid", uid, f_balance)

        self.redis_client.release(lock)
        
        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

 

