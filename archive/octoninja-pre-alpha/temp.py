import sql_functions
imei = '863070011991451'
data = 'imei:863070011991451,tracker,1301020229,,F,182949.000,A,3205.5019,N,03447.3352,E,21.00,11.0,;' 

print 'testing function sql_functions.write_location_to_log(imei,data)...'
res = sql_functions.write_location_to_log(imei,data)
print 'function returned: ' + res
sql_functions.check_alerts(res)
