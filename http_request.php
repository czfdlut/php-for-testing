<?php
/****************************************/
/* purpose: API for HTTP(s) */
/* author:  chenzhifeng */
/* date:    2017-6-16 */
/****************************************/

function http_get_request_with_header($url, $timeout, $header, &$data)
{
    $curl = curl_init();  
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_TIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_CONNECTTIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_DNS_CACHE_TIMEOUT, 300);
    curl_setopt($curl, CURLOPT_NOSIGNAL, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_BINARYTRANSFER, true);
    //curl_setopt($curl, CURLOPT_HEADER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $header);
    //print_r($header);
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); //不验证证书
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); //不验证证书
    $data = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    return $http_code;
}

function http_get_request($url, $timeout, &$data)
{
    $curl = curl_init();  
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_TIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_CONNECTTIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_DNS_CACHE_TIMEOUT, 300);
    curl_setopt($curl, CURLOPT_NOSIGNAL, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_BINARYTRANSFER, true);  
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); //不验证证书
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); //不验证证书
    $data = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    return $http_code;
}

function http_post_request($url, $timeout, &$post_data)
{
    $curl = curl_init();  
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_TIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_CONNECTTIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_DNS_CACHE_TIMEOUT, 300);
    curl_setopt($curl, CURLOPT_NOSIGNAL, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_BINARYTRANSFER, true);  
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); //不验证证书
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); //不验证证书
    curl_setopt($curl, CURLOPT_POST, true);
    curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
    $data = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    return $http_code;
}

function http_post_request_with_header($header, $url, $timeout, &$post_data, &$ret_data)
{
    $curl = curl_init();  
    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_TIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_CONNECTTIMEOUT_MS, $timeout); //毫秒超时
    //curl_setopt($curl, CURLOPT_DNS_CACHE_TIMEOUT, 300);
    curl_setopt($curl, CURLOPT_NOSIGNAL, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_BINARYTRANSFER, true);  
    curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false); //不验证证书
    curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, false); //不验证证书
    curl_setopt($curl, CURLOPT_POST, true);
    if (isset($header)) {
	curl_setopt($curl, CURLOPT_HTTPHEADER, $header); 
    }
    curl_setopt($curl, CURLOPT_POSTFIELDS, $post_data);
    $ret_data = curl_exec($curl);
    $http_code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
    curl_close($curl);
    return $http_code;
}


?>

