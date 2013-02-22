<?php

/*
 * SQL handler class
 * connects to database, and executes various queries
 */

class SQLHandler
{
    private $link;
    
    function connect()
    {
        $this->link = mysql_connect('localhost', 'root', 'root');
        if (!$this->link) 
        {
            die('Could not connect: ' . mysql_error());
        }
        
        mysql_select_db("gpstracker", $this->link);
        
    }
    
    function close()
    {
        mysql_close($this->link);        
    }
    
    function get_units($user_id)
    {
        $query = 'SELECT *  FROM unit_owner LEFT JOIN unit  ON (unit_owner.unit_id = unit.unit_id) WHERE user_id=' . $user_id; 
        //echo 'query: ' . $query . '<br>';
        $result = mysql_query($query);
        //echo 'result:' . $result . '<br>';
        return $result;
    }
    
    function get_unit_last_location($unit_id)
    {
        $query ='SELECT *, AsText(utm) AS utm_text  FROM location_log WHERE unit_id = ' . $unit_id . ' ORDER BY  timestamp DESC LIMIT 1';
        
        //echo 'query: ' . $query . '<br>';
        $result = mysql_query($query);
        //echo 'result:' . $result . '<br>';
        return $result;
        
    }
    
    function parse_sql_point($point)
    {
        $result = trim($point,"()A..Z");
        
        return explode(' ', $result);
        
    }
}




?>
