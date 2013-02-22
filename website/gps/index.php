<?php 
require_once 'sql.php';
?>
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html { height: 100% }
      body { height: 100%; margin: 0; padding: 0 }
      #map_canvas { height: 100% }
    </style>
    <script type="text/javascript">
      function initialize() {
        var mapOptions = {
          center: new google.maps.LatLng(32.194209,34.859619),
          zoom: 14,
          mapTypeId: google.maps.MapTypeId.HYBRID 
        };
        var map = new google.maps.Map(document.getElementById("map_canvas"), mapOptions);
      }

	  function loadScript() {
		  var script = document.createElement("script");
		  script.type = "text/javascript";
		  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyAeIszTTR7abiVR8Xq3HiOEqv-3RyeNU1U&sensor=false&callback=initialize";
		  document.body.appendChild(script);
		}

		window.onload = loadScript;
	  </script>
  </head>
  <body onload="loadScript()">
    <div id="map_canvas" style="width:50%; height:100%; float:left;"></div>
    <div style="width:50%; height:100%; float:right;">
        <div style="height:70%; float: top; background-color:#ffccff"> 
        <?php 
         $conn = new SQLHandler();
         $conn->connect();
         $user_units = $conn->get_units('1');   
         echo '<br><ul>';
         while ($row = mysql_fetch_array($user_units))
         {
             $last_location = mysql_fetch_array($conn->get_unit_last_location($row['unit_id']));
             $lat_long = $conn->parse_sql_point($last_location['utm_text']);
             
             echo '<li>' . $row['name'] . ': ' . $lat_long[0] . ' '. $lat_long[1] . '</li>' ; 
         }
         echo '</ul>';
         $conn->close();           
        ?>

        </div>
        <div style="height:30%; float: bottom; background-color:#9999ff;">  </div>
    </div>
  </body>
</html>