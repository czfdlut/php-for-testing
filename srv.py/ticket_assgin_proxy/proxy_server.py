# -*- coding: utf-8 -*
from mysql_client import MySqlClient
from redis_client import RedisClient
from req_order_ticket import ReqOrderTicket
from order_cancel import OrderCancel
from order_cancel2 import OrderCancel2
from util import logger_handler
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import configparser
from datetime import datetime
from tornado.httpclient import AsyncHTTPClient

tornado.options.define("port", default=9002, type=int, help="port")
tornado.options.define("bind", default="0.0.0.0", help="address bind to")
tornado.options.define("debug", help="0:info | 1:debug", type=int, default=0)
tornado.options.define("publish", help="0:test | 1:online", type=int, default=0)

class Test1Handler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch('https://www.baidu.com')
        print('response: ', response.body)

class StatusCheck(tornado.web.RequestHandler):
    @property
    def logger(self):
        return self.application.logger

    @tornado.gen.coroutine
    def get(self):
        print("headers: ", self.request.headers)
        self.finish("proxy server ok\n")

    @tornado.gen.coroutine
    def post(self):
        print("headers: ", self.request.headers)
        self.finish("proxy server ok\n")

class EventApplication(tornado.web.Application):
    def __init__(self):
        log_name = "proxy_sever_test"
        config_path = "./conf/config_test.conf"
        if tornado.options.options.publish == 1:
            config_path = "./conf/config.conf"
            log_name = "proxy_sever"

        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
            log_path = self.config.get("LOG", "path")
        except Exception as e:
            raise Exception(e)

        self.logger = logger_handler(log_name, logpath=log_path, debug=tornado.options.options.debug)

        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)

        self.redis_client = RedisClient(config_path, "REDIS", self.logger)

        self.redis_client.connect()
        self.mysql_db.connect()

        tornado.web.Application.__init__(self, [
            (r"/status", StatusCheck),
            (r"/Ticket/reqOrderTicket.json", ReqOrderTicket),
            (r"/Ticket/orderCancel.json", OrderCancel),
            (r"Ticket/orderCancel2.json", OrderCancel2),
            (r"/test", Test1Handler),
        ])

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = EventApplication()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port, tornado.options.options.bind)
    tornado.ioloop.IOLoop.current().start()
