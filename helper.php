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

function make_form_request_v2($content, &$header, &$body)
{
    $boundary = "-----------------------------7d83e2d7a141e";
    $multipart_header_fmt = "multipart/form-data; boundary=%s";
    $multipart_fmt = "--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n";
    $multipart_end_fmt = "--%s--\r\n";
    $header = sprintf($multipart_header_fmt, $boundary);
    $body = "";
    foreach($content as $key => $value) 
    {
        if ($key != "param") 
        {
            $tmp = sprintf($multipart_fmt, $boundary, $key, $value);
            $body = $body.$tmp;
        }
        else
        {
            $new_value = json_encode($value);
            $tmp = sprintf($multipart_fmt, $boundary, $key, $new_value);
            $body = $body.$tmp;
        }
    }
    $tmp = sprintf($multipart_end_fmt, $boundary);
    $body = $body.$tmp;
}

function request_xiti($header, $uri, $post_data, $timeout_ms, $retry_cnt, &$ret_data)
{
    print_r("header=");
    print_r($header);
    print_r("\n");
    print_r("uri=".$uri."\n");
    print_r("body=");
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

