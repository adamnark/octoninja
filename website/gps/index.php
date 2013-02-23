<?php 

/*
 * we assume this page is loaded with a specific user_id in mind. for now, 
 * we use user_id = 1
 */

$default_user_id = '1';
require_once 'DataFetcher.php';

$datafetcher = new DataFetcher();
$units_to_print = $datafetcher->get_user_units($default_user_id);
$user_details = $datafetcher->get_user_details($default_user_id);
$default_center_point[0] = '32.047818';
$default_center_point[1] = '34.761265';

if (count($units_to_print) > 0)
{
    $default_center_point[0] = $units_to_print[0]['lat'];
    $default_center_point[1] = $units_to_print[0]['long'];
}


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
    <script src="http://maps.google.com/maps?file=api&v=2&key=AIzaSyAeIszTTR7abiVR8Xq3HiOEqv-3RyeNU1U" type="text/javascript"></script>
    <script type="text/javascript">
         //<![CDATA[
           var map;
           function load() {
              if (GBrowserIsCompatible()) {
                map = new GMap2(
                document.getElementById("map_canvas"));
                map.addControl(new GSmallMapControl());
                map.setCenter(
                new GLatLng(<?php echo $default_center_point[0] ?>, <?php echo $default_center_point[1] ?>), 15);
                
                function createMarker(point, text, title) {
                  var marker =
                  new GMarker(point,{title:title});
                  GEvent.addListener(
                  marker, "click", function() {
                    marker.openInfoWindowHtml(text);
                  });
                  return marker;
                }
                
                <?php
                foreach ($units_to_print as $unit) {
                ?>
                var marker = createMarker(
                new GLatLng(<?php echo $unit['lat'] ?>, <?php echo $unit['long'] ?>),
                '<?php echo $unit['timestamp']?> <br> <?php echo $unit['speed']?> kph',
                '<?php echo $unit['name'] ?>');
                map.addOverlay(marker);
                <?php } ?>
              }
            }
            
            function changeView(lat, lng)
            {
                map.panTo(new GLatLng(lat,lng));
            }
            //]]>   

	  </script>
  </head>
  <body onload="load()" onunload="GUnload()" >
    <div id="map_canvas" style="width:60%; height:100%; float:left;"></div>
    <div style="width:40%; height:100%; float:right;">
        <div style="height:70%; float: top; background-color:#ffffa0; padding-top: 15px; padding-left: 15px;"> 
        <?php 
        $user_name = $user_details['first_name'] .' '.$user_details['last_name'];
        echo '<h2>'.$user_name.'\'s Vehicles:</h1>';
        echo '<ul>';
        foreach ($units_to_print as $unit)
        {
            echo '<li><a href=# onclick="changeView(' .$unit['lat'] .', '. $unit['long']. ')">' . $unit['name'] . '</a></li>';
             
        }
        echo '</ul>';
        ?>

        </div>
        <div style="height:30%; float: bottom; background-color:#ffffaf;">  </div>
    </div>
  </body>
</html>