########################################################################################################################	
def isLogOnReq(data): 
	if data[0:7]=="##,imei:" and data[23:25] == ",A;" :
		return 1
	else:
		return 0
"""  ##,imei:***************,A;  """
########################################################################################################################	
def isHeartbeat(data):	""only imei""
	***************

########################################################################################################################
def iHelpMe(data):	"""Both with or without location"""
	if data[0:4] == "imei:" and data[20:28] == ",help me," :
		return 1
	else:
		return 0
		
	"""  imei:***************,help me,000000000,13554900601,L,;   """
	"""  imei:***************,help me,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;     """
########################################################################################################################	
def isLowBattery(data): ""Both with or without location""
	if data[0:4] == "imei:" and data[20:32] == ",low battery," :
		return 1
	else:
		return 0

	"""  imei:***************,low battery,000000000,13554900601,L,;   """
	"""  imei:***************,low battery,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;   """ 
########################################################################################################################	
def isPosition(data):	
	if data[0:4] == "imei:" and data[20:28] == ",tracker," :
		return 1
	else:
		return 0
	imei:***************,tracker,0809231929,13554900601,F,112909.397,A,2234.4669,N,11354.3287,E,0.11,;  
	imei:***************,tracker,000000000,13554900601,L,;

########################################################################################################################	
""Geo-fence \ move \ speed - not from device""	
imei:***************,stockade,000000000,13554900601,L,;
imei:***************,stockade,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,; 
imei:***************,move,000000000,13554900601,L,;
imei:***************,move,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;
imei:***************,speed,000000000,13554900601,L,;
imei:***************,speed,0809231429,13554900601,F,062947.294,A,2234.4026,N,11354.3277,E,0.00,;
	