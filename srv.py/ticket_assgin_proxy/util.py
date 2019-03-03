# -*- coding: UTF-8 -*-
import logging.config
import os
import yaml
import hashlib
from datetime import datetime
import json
from collections import OrderedDict
import time
import urllib.request
import http.client
import socket

def sha256(url):
    m = hashlib.sha256()
    m.update(url)
    return m.hexdigest()
                
def logger_handler(keyword, logpath="log", debug=0):
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)
    os.chdir("./")
    
    with open('./conf/logging.yaml', 'r') as f:
        yaml_config = yaml.load(f) 
 
    config  = json.dumps(yaml_config)
    config = config.replace("XXXXX", keyword)
    jconfig = json.loads(config)
        
    rkeyword = u"app_%s" % keyword
    jconfig["handlers"][rkeyword]["filename"] = os.path.join(logpath, keyword + ".log") 
    if debug == 1:
        jconfig["loggers"][keyword]["handlers"].append("console") 
    
    logging.config.dictConfig(jconfig)
            
    return logging.getLogger(keyword)

###http://10.16.111.184:11086/engine/detailCheck?_id=11&limit=select_conf&time=1540367559&token=fb36727baeafbfbfeeb06971e77eed6b&_xdebug=true
def get_notify_token(secret_key, _id):    
    timestampe = int(time.time())
    params = OrderedDict({"_id":_id, "limit": "inster_conf", "time": timestampe})    
    lst = sorted(params.items(), key=lambda item: item[0])   
    reqest_param = OrderedDict(lst)
    
    md5_data = ""
    for key in reqest_param.keys():
        md5_data = md5_data + str(reqest_param[key])
    sign = md5(md5_data + secret_key)
    return sign, timestampe

def md5(url):
    m = hashlib.md5(url)
    return m.hexdigest()

def request_query(url, headers={}, data=None, timeout=30):
    try:
        req = urllib.request.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        resp = urllib.request.urlopen(req, data=data, timeout=timeout)
        return resp.info(), resp.read(), None
    except (urllib.request.HTTPError, http.client.HTTPException) as err:
        return None, None, err.read()
    except (socket.error, socket.timeout) as err:
        return None, None, str(err)
    except Exception as err:
        return None, Nne, str(err)

if __name__ == "__main__":
    #print("test query: ", request_query("http://127.0.0.1:8888/mod_lucenewriter/_bulk_add", data={"ff": "data"}))
    data = {
      "sign": "MD5MD5MDMD5MD5MDMD5MD5MDMD5MD5MD5",
      "ver": "1.0",
      "timestamp": "137889283",
      "command": "3004",
      "token": "adsdiiosdfw899823sdfa0023sdfkkkasdf98831239",
      "openid": "oB4nYjvY13SVtaWC-AFztM2f3TlU",
      "param": {
        "merchantCode": "00001",
        "merchantName": "携程订票系统",
        "bizNo": "10000123",
        "bizType": " ORDERTICKET ",
        "bizName": "订票",
        "bizBrief": "用户订票",
        "bizTime": "2018-09-01 12:12:12",
        "orderNo": "0000000",
        "orderType ": "0",
        "orderDate": "2018-09-01",
        "fromStation": "西安",
        "toStation": "北京西",
        "tranCode": "G666",
        "trainType": "1",
        "seatType": "O",
        "startTime": "2018-09-01 12:12:12",
        "endTime": "2018-09-01 18:12:12",
        "ticketTime ": "2018-09-01 12:12:12",
        "noSeatFlag": "Y",
        "ticketNum": "1",
        "idType": "1",
        "idNo": "1:430224190001011111#2:430224190001011111",
        "idName": "张三",
        "ticketPrices": "368.5",
        "couponValue": "50.0",
        "bonusFlag": "2.0",
        "serviceFee": "5.0",
        "insureFee": "3.0",
        "expressFee": "10.0",
        "payType": "1",
        "userId": "1111",
        "mobile": "13800138000",
        "address": "陕西渭南",
        "requestID": "20180606000005",
        "ticketObtainMode": "1",
        "officeId": "2",
        "ticketTakePoint": "1",
        "reserved": "预留",
        "haiNum": "1",
        "allocationFlag": "Y",
        "remark": "备注"
      }
    }

    headers = {"Content-Type":"application/json"}
    post_data = bytes(json.dumps(data), 'utf8') 
    resp_headers, result, err = request_query("http://127.0.0.1:8888/Ticket/reqOrderTicket.json", 
                            headers=headers,
                            data=post_data, timeout=30)
    print("result: ", result)
    print("type: ", type(result))
    print("ss: ", json.loads(result)["errcode"])
    #import requests
    #resp = requests.post("https://www.xt-kp.com/Ticket/reqOrderTicket.json", data=json.loads(post_data), headers=headers)
    #print("resp: ", resp.text)
     
