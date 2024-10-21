import sys
import fileinput


for line in fileinput.input():
    print(line.strip())
quit()

try:
	for line in iter(sys.stdin.readline, b''):
		print(line)
		
except KeyboardInterrupt:
	sys.stdout.flush()
	pass

