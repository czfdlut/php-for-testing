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

function make_form_request($content)
{
    $message = array();
    foreach($content as $key => $value) 
    {
        $pair = "";
        if ($key != "param") 
        {
            $message[$key] = $value;
        }
        else
        {
            $tmp = json_encode($value);
            $message[$key] = $tmp;
        }
    }
    return $message;
}

function request_xiti($header, $uri, $post_data, $timeout_ms, $retry_cnt, &$ret_data)
{
    print_r("uri=".$uri."\n");
    print_r("post=");
    print_r($post_data);
    print_r("\n");
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

