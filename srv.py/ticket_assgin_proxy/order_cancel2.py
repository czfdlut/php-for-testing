# -*- coding: utf-8 -*
from datetime import datetime
import tornado.web

class OrderCancel2(tornado.web.RequestHandler):     
    @property
    def logger(self):
        return self.application.logger

    @property
    def mysql_db(self):
        return self.application.mysql_db

    @property
    def config(self):
        return self.application.config

    @tornado.gen.coroutine
    def post(self):
        param = self.get_argument('param')
        print(type(param))
        print(param)
        param = eval(param)
        print(type(param))
        print(param)
        self.write('OK')

    


