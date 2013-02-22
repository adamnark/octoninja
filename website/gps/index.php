<?php 

/*
 * we assume this page is loaded with a specific user_id in mind. for now, 
 * we use user_id = 1
 * 
 */

$default_user_id = '1';
require_once 'DataFetcher.php';

$datafetcher = new DataFetcher();
$units_to_print = $datafetcher->get_user_units($default_user_id);

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
          center: new google.maps.LatLng(<?php echo $units_to_print[0]['lat'] ?>, <?php echo $units_to_print[0]['long'] ?>),
          zoom: 17,
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
    <div id="map_canvas" style="width:60%; height:100%; float:left;"></div>
    <div style="width:40%; height:100%; float:right;">
        <div style="height:70%; float: top; background-color:#ffccff"> 
        <?php 
        
        echo '<br><ul>';
        foreach ($units_to_print as $unit)
        {
            echo '<li>' . $unit['name'] . ' was last seen at: ' . $unit['lat'] . ' ' . $unit['long'] . '</li>';
             
        }
        echo '</ul>';
        fclose($f); 
        
        ?>

        </div>
        <div style="height:30%; float: bottom; background-color:#9999ff;">  </div>
    </div>
  </body>
</html>