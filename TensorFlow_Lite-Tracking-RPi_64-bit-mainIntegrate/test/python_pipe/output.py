import time
import sys
i = 0

while (i < 5):
	print(f"{i} iterations complete", file=sys.stdout)
	sys.stdout.flush()
	time.sleep(1)
	i+=1
