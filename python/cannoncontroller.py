import re
import time

def validateCommandIsKeyword(cmd):
	return cmd in ["up", "down", "left", "right", "stop", "fire"]

def performCommand(cmd, delay):
	print("Sending command '" + cmd + "'")
	if delay:
		print(f"sleeping {delay}")
		time.sleep(delay/1000)
		print("Sending 'stop'")
	print("OK")

cmdPattern = re.compile("^([a-z]+)( ([0-9]+))?$")
print(">> Cannon Controller. Use commands up, down, left, right, stop and fire with an optional duration")
while True:
	cmdLine = input()
	match = cmdPattern.match(cmdLine)
	if match:
		cmd = match.group(1)
		if not validateCommandIsKeyword(cmd):
			print("ERROR: Command is not in up, down, left, right, stop, fire")
		else:
			durationStr = match.group(3)
			if durationStr:
				duration = int(durationStr)
				if cmd == "fire" or cmd == "stop":
					print("ERROR: 'fire' and 'stop' does not take arguments")
				else:
					if duration > 10000:
						print("ERROR: Delay must not be greater than 10000")
					else:
						performCommand(cmd, duration)
						#print("cmd: '" + cmd + "', arg: '" + arg + "'")
			else:
				performCommand(cmd, None)
			#print("cmd: '" + cmd + "'")
	else:
		print("ERROR: Invalid command")
