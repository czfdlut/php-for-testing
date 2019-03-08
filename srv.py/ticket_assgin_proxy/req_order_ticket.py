# -*- coding: utf-8 -*
from util import request_query
import tornado.web
from datetime import datetime
import json
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

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": "bbb", "data": {}})
        self.finish()

    def content_type_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "content-type":
                return {k: v}
        return {}

    def param_request_parm(self):
        try:
            param = json.loads(self.get_argument("param"))
        except Exception as err:
            return "Error: %s" % err, None

        if "ticketPrices" not in param:
            return "Error: not found ticketPrices", None

        if float(param["ticketPrices"]) < 1.0 or float(param["ticketPrices"]) > 3000:
            return "Error: money out of money", None

        if "merchantCode" not in param:
            return "Error: not found merchantCode", None

        if "bizNo" not in param:
            return "Error: not found bizNo", None

        if "bizName" not in param:
            return "Error: not found bizName", None

        if "bizTime" not in param:
            return "Error: not found bizTime", None

        if "orderDate" not in param:
            return "Error: not found orderDate", None

        if "ticketPrices" not in param:
            return "Error: not found ticketPrices", None

        if "payType" not in param:
            return "Error: not found payType", None

        if "requestID" not in param:
            return "Error: not found requestID", None

        return None, param

    def join_db_data(self, uid, param, server_resp_data):
        hdata = {"uid": uid}
        try:
            resp_data = json.loads(server_resp_data)
            hdata["errmsg"]  = resp_data["errmsg"]
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

    def add_headers(self, headers, k, v):
        is_exist_kv = False
        for k ,v in headers.items():
            if k.lower() == k.lower():
                is_exist_kv = true

        if is_exist_kv:
            headers[k] = v

    @tornado.gen.coroutine
    def reqeust_proxy_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=self.timeout)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()

        uid = self.get_uid_from_headers()
        self.logger.info("ticket uid: %s url: %s " % (uid, self.url))

        sql = "select balance from account_balance where uid='%s' and balance>1.0 limit 1" % uid
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            self.finish_err_msg(r"非法uid")
            return

        self.logger.info("account balance: %s" % qs[0][0])

        err, param = self.param_request_parm()
        if err is not None:
            self.logger.error(err)
            self.finish_err_msg(r"参数错误")
            return

        self.logger.info("reqeust_body: %s " % self.request.body)

        balance_uid = "ticket-uid_%s" % uid
        trans_balance = self.redis_client.get(balance_uid)
        if trans_balance is None:
            self.logger.error("not found ticket_balance: %s" % balance_uid)
            self.finish_err_msg(r"金额错误")
            return

        self.logger.info("trans_balance: %s" % float(trans_balance))

        cur_balance = self.redis_client.hget("ticket-uid", uid)
        if len(cur_balance) == 0:
            self.finish_err_msg(r"金额错误")
            return

        self.logger.info("lock_balance: %s" % cur_balance)

        ticket_prices = float(param["ticketPrices"])
        if float(trans_balance) < ticket_prices or float(cur_balance) < ticket_prices:
            self.finish_err_msg(r"金额超限")
            return

        self.logger.info("ticket_prices: %f" % ticket_prices)
        trans_after_balance = self.redis_client.incrbyfloat(balance_uid, -1.0 * ticket_prices)
        if trans_after_balance is None:
	        self.finish_err_msg(r"交易非法")
	        return
	    
        if float(trans_after_balance) < 0.01:
            self.redis_client.incrbyfloat(balance_uid, ticket_prices)
            self.finish_err_msg(r"交易非法")
            return

        headers = self.content_type_from_headers()
        resp_headers, resp_data, err = yield tornado.gen.Task(self.reqeust_proxy_server, headers, self.request.body)

        self.logger.info("resp_headers: %s" % str(resp_headers))
        self.logger.info("resp_data: %s" % str(resp_data))

        if err is not None:
            self.logger.error("request error:%s" % err)
            self.redis_client.incrbyfloat(balance_uid, ticket_prices)
            self.write(err)
            self.finish()
            return

        self.add_headers(resp_headers, "Content-Type", "application/json;charset=UTF-8")
        self.set_response_header(resp_headers)
        self.set_response_status(200)

        hdata = self.join_db_data(uid, param, resp_data)
        self.logger.info("hdata: %s" % json.dumps(hdata))

        if hdata is None or hdata["status"] == 0:
            elf.redis_client.incrbyfloat(balance_uid, ticket_prices)

        if hdata is None:
            self.logger.error("db data error")
            self.write(resp_data)
            self.finish()
            return

        lock = self.redis_client.acquire("ticket-uid_%s_lock" % uid, 1)
        self.mysql_db.insert("order_ticket", hdata)
        self.redis_client.release(lock)

        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))
