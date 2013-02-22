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
        $f = fopen('fetcher log.txt', 'w');
        
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
            $i++;
        }

        $this->conn->close();     
        fclose($f);
        return $units_to_print;
    }
}





?>