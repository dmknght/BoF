import sys, itertools
from pwn import *
context.log_level = "error"

#Todo get $eip / $rip

def printHelpBanner():
	print('''Usage:
	%s <Target file> <Input type>

Target file is an executable file
Input type must be argv or input''' % sys.argv[0])

def printCrashedOutput(txtErrCode, txtLastMsg, txtPayload, txtPayloadLength):
	print('''
		Exit code: %s,
		Stdout: [ %s ],
		Payload Length: %s,

Payload: %s
		''' %(txtErrCode, txtLastMsg, txtPayloadLength, txtPayload))

def getPatternLength(txtPayload, txtRegisterValue):
	txtBuf, txtRegisterValue, _ = txtPayload.partition(txtRegisterValue)
	sizeBuf = len(txtBuf)
	return sizeBuf
	#TODO better pattern size

def generatePayload(payloadLength):
	retPayloadText = ''
	count = 0
	for objGenPatter in itertools.product(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], ['A', 'B', 'C', 'D', 'E', 'F'], ['A', 'B', 'C', 'D', 'E', 'F']):
		retPayloadText += ''.join(objGenPatter)
		if count >= payloadLength / 4:
			break
		count += 1
	return retPayloadText[:payloadLength]

def fuzzDump(txtFileFuzz, txtPayload, txtInputType):
	# objFileFuzz: full file path to executable file
	# objPayload: payload after generating
	# objInputType: input way: argv / input
	if txtInputType == 'argv':
		#edit here if need other param
		objFuzzProcess = process([txtFileFuzz, txtPayload])
	else:
		objFuzzProcess = process(txtFileFuzz)
		# Edit here if need other input
		objFuzzProcess.sendline(txtPayload)
	objFuzzProcess.shutdown()
	txtFuzzMsg = objFuzzProcess.recvall().split('\n')
	txtFuzzErrCode = objFuzzProcess.poll()
	return ' '.join(txtFuzzMsg).split('\n'), txtFuzzErrCode

def handlerFuzzRequest(txtTargetName, txtInputType):
	for varPayloadLength in range(1, 14400):
		txtFuzzPayload = generatePayload(varPayloadLength)
		txtLastMsg, txtErrCode = fuzzDump(txtTargetName, txtFuzzPayload, txtInputType)
		if txtErrCode != 1 and txtErrCode != 0:
			# Todo: Better interrupt program
			printCrashedOutput(txtErrCode, txtLastMsg, txtFuzzPayload, varPayloadLength)
			break
	# Get $eip / $rip
	# Get offset

def main():
	if len(sys.argv) != 3:
		printHelpBanner()
	else:
		try:
			optTargetPath = sys.argv[1]
			optFuzzMethod = sys.argv[2]
			if optFuzzMethod not in ['input', 'argv']:
				print("Unknow method. Must be [ argv / input ]")
			else:
				handlerFuzzRequest(optTargetPath, optFuzzMethod)
		except KeyboardInterrupt:
			print("Stop by user")
			sys.exit()
		except:
			print("Unknow error")

main()
