<?php

function display($content)
{
    foreach($content as $key => $value) 
    {
	    print_r($key."=>");
        print_r($value);
        print_r("\n");
    }
}

function create_sign($content, $extra_code)
{
    ksort($content);
    
    $message = "";
    foreach($content as $key => $value) 
    {
        if ($key != "sign") 
        {
            if ($key != "param") {
	            $message = $message.$value;
            } else {
                $tmp = json_encode($value);
                $message = $message.$tmp;
            }
        }
    }
    $message = $message.$extra_code;
    //print_r($message."\n");
    $sign = md5($message);
    //print_r($sign);
    
    return $sign;
}

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

function make_request($content)
{
    $message = "";
    foreach($content as $key => $value) 
    {
        $pair = "";
        if ($key != "param") 
        {
            $pair = $key."=".$value;
        }
        else
        {
            $tmp = json_encode($value);
            $pair = $key."=".$tmp;
        }
        if ($message != "") {
            $message = $message."&".$pair;
        } else {
            $message = $pair;
        }
    }
    return $message;
}

function request_xiti($header, $uri, $post_data, $timeout_ms, $retry_cnt, &$ret_data)
{
    print_r("uri=".$uri."\n");
    print_r("post=".$post_data."\n");
    $ec = -1;
    while (true) {
        $ec = http_post_request_with_header($header, $uri, $timeout_ms, $post_data, $ret_data);
        if ($ec == 200 || --$retry_cnt <= 0) {
            break;
        }
    }
    return $ec;
}

?>

