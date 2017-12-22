import sys, time
from pwn import *
context.log_level = "error"

def help():
	print '''
	Usage:
		{} filename <input / argv>
'''

def verbose(length, payload, _msg):
		print '''
		Length: {},
		Payload: {},
		Output: {},
		'''.format(length, payload, _msg)
		time.sleep(0.6)

def _error_code_unknown(_err_code, _msg, payload, length):
	print '''
	Segmentation fault
	Exit_code: {},
	Stdout: {},
	Payload length: {},
	Buf size: {}
	Exit!
	'''.format(_err_code,'\n'.join( _msg), len(payload), length)

def _diff_stdout(first_msg, _msg, payload, length):
			print '''
			Recv different output
			First stdout: {},
			Stdout: {},
			Payload length: {},
			Buf size: {}
			'''.format(first_msg, _msg[-1], len(payload), length)

def _output(filename, payload):
	_fuzz = process(filename)
	_fuzz.sendline(payload)
	_fuzz.shutdown()
	_tmp = _fuzz.recvall().split('\n')
	_err_code = _fuzz.poll()
	return ' '.join(_tmp).split(), _err_code

def argv_output(filename, payload):
	#edit here for each time try new 
	_fuzz = process([filename, payload])
	_fuzz.shutdown()
	_tmp = _fuzz.recvall().split('\n')
	_err_code = _fuzz.poll()
	return ' '.join(_tmp).split(), _err_code

def fuzz_input(filename):
	first_msg, _err_code = _output(filename, 'a40Jg8az')
	try:
		first_msg = first_msg[-1]
	except:
		pass

	for length in range(0, 2048):
		payload = 'a' * length + 'a'
		_msg, _err_code = _output(filename, payload)
		try:
			_last_msg = _msg[-1]
		except:
			_last_msg = _msg
		if _err_code != 0 or _err_code != 1:
			_error_code_unknown(_err_code, _msg, payload, length)
			break
		elif _last_msg != first_msg:
			_diff_stdout(first_msg, _msg, payload, length)
			_choose = raw_input('[C]ontinue / [S]how full stdout ').replace('\n', '')
			if (_choose == 'c') or (_choose == 'C'):
				first_msg = _msg[-1]
				pass
			elif (_choose == 's') or (_choose == 'S'):
				print '\n'.join(_msg)
				raw_input('[Enter] to continue or [Ctrl] + [C] to quit')
				first_msg = _last_msg
			else:
				print "Invalid option, exit"
				break
		else:
			pass


def fuzz_argv(filename):
	first_msg, error_code = argv_output(filename, 'aos&79A')
	try:
		first_msg = first_msg[-1]
	except:
		pass
	for length in range(0, 2048):
		payload = 'a' * length + 'a'
		_msg, _err_code = argv_output(filename, payload)
		try:
			_last_msg = _msg[-1]
		except:
			_last_msg = _msg
		if _err_code == -11:
			_error_code_unknown(_err_code, _msg, payload, length)
			break
		elif _last_msg != first_msg:
			_diff_stdout(first_msg, _msg, payload, length)
			_choose = raw_input('[C]ontinue / [S]how full stdout ').replace('\n', '')
			if (_choose == 'c') or (_choose == 'C'):
				first_msg = _msg[-1]
				pass
			elif (_choose == 's') or (_choose == 'S'):
				print '\n'.join(_msg)
				raw_input('[Enter] to continue or [Ctrl] + [C] to quit')
				first_msg = _last_msg
			else:
				print "Invalid option, exit"
				break
		else:
			pass

def main():
	if len(sys.argv) != 3:
		help()
	else:
		try:
			filepath = sys.argv[1]
			method = sys.argv[2]
			if method == "input":
				fuzz_input(filepath)
			elif method == "argv":
				fuzz_argv(filepath)
			else:
				print "Unknown method"
		except KeyboardInterrupt:
			print "Bye"
			sys.exit()

main()
