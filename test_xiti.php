<?php

require("http_request.php");
require("helper.php");


$appid = '35385640507';
$appsecret = 'a14c4ab485a60833fe09064e27ae013e';
$extra_code = 'abx23579436';


/* 获得token */
function get_access_token()
{
    global $appid, $appsecret, $extra_code;
    $cmd = '1001';
    $openid = '';
    $timestamp = time(); //'1550130142439';
    $token = '';
    $ver = '1.0';
    $sign = '';
        
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'param' => array(
            'appid' => $appid,
            'secret' => $appsecret
        ),
        'timestamp' => $timestamp,
        'openid' => $openid
    );
    //display($content);

    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    //display($content);

    $post_data = json_encode($content);
    //print_r($post_data);
    $uri = "https://www.xt-kp.com/base/doAction";
    $header = array(
	    "Content-type: application/json;charset='utf-8'", 
	    "Accept: application/json", 
	    "Cache-Control: no-cache", 
	    "Pragma: no-cache", 
    );
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

    $ret_array = json_decode($ret_data, true);
    //print_r($ret_array);
    return $ret_array['data']['token'];
}


/* 申请订票 */
function req_order_ticket($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '3004';
    $token = $access_token;
    $openid = '';
    
    $merchantCode = $appid;
    $merchantName = "美团订票系统";
    $bizNo = "20190302";
    $bizType = 'DP';
    $bizName = '订票';
    $bizBrief = '用户订票';
    $bizTime = date("Y-m-d h:i:s");
    $orderNo = '0000000';
    $orderType = '0';
    $orderDate = date("Y-m-d");
    $fromStation = '西安';
    $toStation = '北京西';
    $trainCode = 'G666';
    $trainType = 'G';
    $seatType = '0';
    $tomorrow = strtotime("tomorrow");
    $startTime = date("Y-m-d h:i:s", $tomorrow);
    $endTime = $startTime;
    $ticketTime = $startTime;
    $ticketType = '1';
    $noSeatFlag = 'Y';
    $ticketNum = '1';
    $idType = '1';
    $idNo = '1:440101200702060011';
    $IdName = '张三';
    $ticketPrices = '68.5';
    $couponValue = "50.0";
    $bonusFlag = '2.0';
    $serviceFee = '5.0';
    $insureFee = '3.0';
    $expressFee = '10.0';
    $payType = '1';
    $mobile = '18688886666';
    $userId = '1111';
    $address = '陕西渭南';
    $requestID = '20190302';
    $ticketObtainMode = '1';
    $officeId = '2';
    $ticketTakpePoint = '1';
    $reserved = '预留';
    $haiNum = 0;
    $allocationFlag = 'Y';
    $remark = "备注";
        
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'appid' => $appid,
            'secret' => $appsecret,
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'bizName' => $bizName,
            'bizBrief' => $bizBrief,
            'bizTime' => $bizTime,
            'orderNo' => $orderNo,
            'orderType' => $orderType,
            'orderDate' => $orderDate,
            'fromStation' => $fromStation,
            'toStation' => $toStation,
            'trainCode' => $trainCode,
            'trainType' => $trainType,
            'seatType' => $seatType,
            'startTime' => $startTime,
            'endTime' => $endTime,
            'ticketTime' => $ticketTime,
            'ticketType' => $ticketType,
            'noSeatFlag' => $noSeatFlag,
            'ticketNum' => $ticketNum,
            'idType' => $idType,
            'idNo' => $idNo,
            'IdName' => $IdName,
            'ticketPrices' => $ticketPrices,
            'couponValue' => $couponValue,
            'bonusFlag' => $bonusFlag,
            'serviceFee' => $serviceFee,
            'insureFee' => $insureFee,
            'expressFee' => $expressFee,
            'payType' => $payType,
            'userId' => $userId,
            'address' => $address,
            'requestID' => $requestID,
            'ticketObtainMode' => $ticketObtainMode,
            'officeId' => $officeId,
            'ticketTakpePoint' => $ticketTakpePoint,
            'reserved' => $reserved,
            'haiNum' => $haiNum,
            'allocationFlag' => $allocationFlag,
            'remark' => $remark
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;
    
    $type = 2;
    $post_data = "";
    $header = array();
    if ($type == 1) 
    {
        $post_data = make_request($content);
        $header = array(
            "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
            "Accept: application/json", 
            "Cache-Control: no-cache", 
            "Pragma: no-cache",
            "ticket-uid: for_test"
        );

    }
    else if ($type == 2)
    {
        $tmp = "";
        make_form_request_v2($content, $tmp, $post_data);
        print_r($tmp."\n");
        print_r($post_data."\n");
        $content_type = sprintf("Content-type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
            "ticket-uid: for_test",
            //"Expect: 100-continue"
        );
    }

    //$uri = "https://www.xt-kp.com/Ticket/reqOrderTicket.json";
    $uri = "http://127.0.0.1:80/Ticket/reqOrderTicket.json";
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");
    
}


/* 上传身份证照片 */
function upload_IdImg()
{
}


/* 订单查询 */
function query_ticket_result($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = '1551432535'; //time(); 
    $cmd = '3006';
    $token = $access_token;
    $openid = '';
    
    $merchantCode = $appid;
    $merchantName = '美团';
    $bizNo = '20190224';
    $bizType = 'DP';
    $bizName = '订票查询';
    $bizBrief = '用户订票';
    $bizTime = '2019-03-01 17:45:10'; //date('Y-m-d H:i:s');
    $orderDate = '2019-03-01';//date('Y-m-d');
    $mobile = '18688886666';
    $orderStatus = '9';
    $startBizTime = '2019-03-01 18:10:10'; //date('Y-m-d');
    $endBizTime = '2019-03-01 20:10:10'; //date('Y-m-d');
    $pageIndex = 0;
    $pageSize = 100;
    $requestID = '20190224';
    
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'appid' => $appid,
            'secret' => $appsecret,
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'bizName' => $bizName,
            'bizBrief' => $bizBrief,
            'bizTime' => $bizTime,
            'orderDate' => $orderDate,
            'mobile' => $mobile,
            'orderStatus' => $orderStatus,
            'startBizTime' => $startBizTime,
            'endBizTime' => $endBizTime,
            'pageIndex' => $pageIndex,
            'pageSize' => $pageSize,
            'requestID' => $requestID
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    //$uri = "https://www.xt-kp.com/Ticket/queryTicketResult.json";
    $uri = "http://127.0.0.1:8080/Ticket/queryTicketResult.json";

    /* 方法1 */
    $type = 1;
    if ($type == 1) 
    {
        $post_data = make_request($content);
        $header = array(
	        "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
    else if ($type == 2) {
        $post_data = make_form_request($content);
        $header = array(
	        "Content-type: multipart/form-data; charset='utf-8'", 
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
    else if ($type == 3)
    {
        $tmp = "";
        $post_data = "";
        make_form_request_v2($content, $tmp, $post_data);
        print_r($tmp."\n");
        print_r($post_data."\n");
        $content_type = sprintf("Content-type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
            "ticket-uid: for_test",
        );
    }
    //print_r($post_data);
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}


/* 订单退单(退单条件：已支付&未出票) */
function cancel_order($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '3007';
    $token = $access_token;
    $openid = '';
        
    $merchantCode = $appid;
    $merchantName = '美团';
    $bizNo = '20190302';
    $bizType = 'DPQX';
    $mobile = '18688886666';
    $orderId  = '0000000'; //20190302';
    $requestID = '20191224';
    
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'mobile' => $mobile,
            'orderId' => $orderId,
            'requestID' => $requestID
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    $type = 2;
    $header = array();
    $post_data = "";
    if ($type == 1)
    {
        $post_data = make_request($content);
        $header = array(
                "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
                "Accept: application/json", 
                "Cache-Control: no-cache", 
                "Pragma: no-cache",
                );
    }
    else if ($type == 2)
    {
        $tmp = "";
        make_form_request_v2($content, $tmp, $post_data);
        $content_type = sprintf("Content-type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
            "ticket-uid: for_test",
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
 
    $ret_data = "";
    //$uri = "https://www.xt-kp.com/Ticket/orderCancel.json";
    #$uri = "http://127.0.0.1:8080/Ticket/orderCancel.json";
    $uri = "http://test.maidaopiao.com/Ticket/orderCancel.json";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}


/* 订单撤单(撤单条件：未支付) */
function cancel_order_v2($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '3007';
    $token = $access_token;
    $openid = '';
        
    $merchantCode = $appid;
    $merchantName = '美团';
    $bizNo = '20190224';
    $bizType = 'DPQX';
    $mobile = '18688886666';
    $orderId  = '20190224';
    $requestID = '20191224';
    
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'mobile' => $mobile,
            'orderId' => $orderId,
            'requestID' => $requestID
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    $post_data = make_request($content);
    $uri = "https://www.xt-kp.com/Ticket/orderCancel2.json";
    $header = array(
	    "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
	    "Accept: application/json", 
	    "Cache-Control: no-cache", 
	    "Pragma: no-cache",
    );
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}

function test()
{
    // 获取token
    $access_token = 'f2c99b55731732bd18a203aa999a2f06'; //get_access_token();
    print_r($access_token."\n");
    $type = 3;
    if ($type == 1) {
        // 申请订票
        req_order_ticket($access_token);
    } else if ($type == 2) {
        // 查询订单
        query_ticket_result($access_token);
    } else if ($type == 3) {
        // 订单退单
        cancel_order($access_token);
    } else if ($type == 4) {
        // 订单撤单
        cancel_order_v2($access_token);
    }

}

test();

?>

