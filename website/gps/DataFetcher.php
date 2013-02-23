<?php

/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

require_once 'SQLHandler.php';

class DataFetcher
{
    private $conn;
    
    function __construct() {
        $this->conn = new SQLHandler();
    }
    
    function get_user_units($user_id)
    {
        $f = fopen('C:\fetcher_log.txt', 'w');
        
        $this->conn->connect();
        fwrite($f, "connection established!\r\n");
        $user_units = $this->conn->get_units($user_id);
        fwrite($f, "got units for user_id=". $user_id ."!\r\n");
        $i = 0;
        $units_to_print = array();
        while ($row = mysql_fetch_array($user_units))
        {
            $last_location = mysql_fetch_array($this->conn->get_unit_last_location($row['unit_id']));
            $lat_long = $this->conn->parse_sql_point($last_location['utm_text']);
            $units_to_print[$i] = array();
            $units_to_print[$i]['lat'] = $lat_long[0];
            $units_to_print[$i]['long'] = $lat_long[1];
            $units_to_print[$i]['name'] = $row['name'];
            $units_to_print[$i]['timestamp'] = $last_location['timestamp'];
            $units_to_print[$i]['speed'] = $last_location['speed'];
            
            fwrite($f, "Fetched row!!\r\n");
            foreach ($units_to_print[$i] as $key => $value) {
                fwrite($f, $key . ": ". $value. '\r\n');
            }
            
            $i++;
        }

        $this->conn->close();     
        fclose($f);
        return $units_to_print;
    }
    
    function get_user_details($user_id)
    {
        $this->conn->connect();
        $result = mysql_fetch_array($this->conn->get_user_details($user_id));
        if (count($result) > 0){
            $user['first_name'] = $result['first_name'];
            $user['last_name'] = $result['last_name'];
            $user['email'] = $result['email'];
        }
        
        $this->conn->close();
        return $user;
    }
}





?>