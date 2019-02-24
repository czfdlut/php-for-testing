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
    print_r($message."\n");
    $sign = md5($message);
    print_r($sign);
    
    return $sign;
}

?>

