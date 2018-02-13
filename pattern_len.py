import sys, itertools

def generatePayload(payloadLength):
	retPayloadText = ''
	count = 0
	for objGenPatter in itertools.product(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['A', 'B', 'C', 'D', 'E', 'F'], ['A', 'B', 'C', 'D', 'E', 'F']):
		retPayloadText += ''.join(objGenPatter)
		if count >= payloadLength / 4:
			break
		count += 1
	return retPayloadText[:payloadLength]



def handlerPatternLength(valuePatternPosition):
	for txtPayloadLength in range(1, 14400):
		txtPayloadTmp = generatePayload(txtPayloadLength)
		if valuePatternPosition not in txtPayloadTmp:
			pass
		else:
			txtBuf, _ = txtPayloadTmp.split(valuePatternPosition)
			print("Buf size: %s" %(len(txtBuf)))
			break
#input: eip value

handlerPatternLength(sys.argv[1])
