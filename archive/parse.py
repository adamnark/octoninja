def parse(packet):
	packet = packet.split(',')
	print '===='
	for i in range(len(packet)):
		print repr(i) + '> ' + packet[i]
	print len(packet)
	return packet

def main():
	d = parse('imei:863070011991451,tracker,1301020229,,F,182949.000,A,3205.5019,N,03447.3352,E,0.00,,;')

if (__name__ == '__main__'):
	main()