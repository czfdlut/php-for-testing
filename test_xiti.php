<?php

require("http_request.php");
require("helper.php");

function get_uri($appkey, $appsecret, $query, $from, $to)
{
    $url = "http://openapi.youdao.com/api?";
    $url = $url."from=".$from;
    $url = $url."&to=".$to;
    $url = $url."&appKey=".$appkey;
    $url = $url."&q=".$query;
    $salt = time();
    $url = $url."&salt=".$salt;
    $sign = strtoupper(md5($appkey.$query.$salt.$appsecret));
    $url = $url."&sign=".$sign;
    print_r("url=".$url."\n");
    //return urlencode($url);
    return $url;
}


function request_xiti($header, $uri, $post_data, $timeout_ms, $retry_cnt, &$ret_data)
{
    print_r("uri=".$uri);
    print_r("post=".$post_data);
    $ec = -1;
    while (true) {
        $ec = http_post_request_with_header($header, $uri, $timeout_ms, $post_data, $ret_data);
        if ($ec == 200 || --$retry_cnt <= 0) {
            break;
        }
    }
    return $ec;
}

function get_token()
{
    $appid = '35385640507';
    $appsecret = 'a14c4ab485a60833fe09064e27ae013e';
    $extra_code = 'abx23579436';
    $cmd = '1001';
    $openid = '';
    $timestamp = '1550130142439';
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
    display($content);

    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    display($content);

    $post_data = json_encode($content);
    print_r($post_data);
    //$uri = get_uri($appkey, $appsecret, $query, $from, $to);
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

}

function test()
{
    get_token();
}

test();

?>

