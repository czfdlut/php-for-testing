import tornado.ioloop
import tornado.web
import json

class ReqOrderTicket(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        print("%s%s?%s" % (self.request.host, self.request.path, self.request.query))
        body = self.request.body
        print("body: ", body)

        self.set_header("Content-Type", "application/json")

        resp_data = {
            "sign":"MD5MD5MDMD5MD5MDMD5MD5MDMD5MD5MD5",
            "ver":"1.0",
            "timestamp":"137889283",
            "command":"3004",
            "errcode":"0",
            "errmsg":"成功",
            "data":{
                "requestID":"20180606000005",
                "orderTicketFlow":"e9569fc049de46bfb52d560d05106ef7"
            }
        }

        self.write(json.dumps(resp_data))
        self.finish()

class OrderCancel(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        print("%s%s?%s" % (self.request.host, self.request.path, self.request.query))
        body = self.request.body
        print("body: ", body)

        self.set_header("Content-Type", "application/json")

        resp_data =  {
            "sign":"MD5MD5MDMD5MD5MDMD5MD5MDMD5MD5MD5",
            "ver":"1.0",
            "timestamp":"137889283",
            "command":"3007",
            "token":"adsdiiosdfw899823sdfa0023sdfkkkasdf98831239",
            "openid":"oB4nYjvY13SVtaWC-AFztM2f3TlU",
            "param":{
                "merchantCode":"00001",
                "merchantName":"携程订票系统",
                "bizNo":"10000124",
                "bizType":" DPQX ",
                "mobile ":"1380013800",
                "orderId":"9",
                "requestID":"20180606000008"
            }
        }

        self.write(json.dumps(resp_data))
        self.finish()

class OrderCancel2(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        print("%s%s?%s" % (self.request.host, self.request.path, self.request.query))
        body = self.request.body
        print("body: ", body)

        self.set_header("Content-Type", "application/json")

        resp_data ={
            "sign":"MD5MD5MDMD5MD5MDMD5MD5MDMD5MD5MD5",
            "ver":"1.0",
            "timestamp":"137889283",
            "command":"3008",
            "errcode":"0",
            "errmsg":"成功",
            "data":{
                "requestID":"20180606000008",
                "orderTicketFlow":"e9569fc049de46bfb52d560d05106ef7",
                "cancelStatus":"0"
            }
        }

        self.write(json.dumps(resp_data))
        self.finish()


def make_app():
    return tornado.web.Application([
        (r"/Ticket/reqOrderTicket.json", ReqOrderTicket),
        (r"/Ticket/orderCancel.json", OrderCancel),
        (r"/Ticket/orderCancel2.json", OrderCancel2),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
