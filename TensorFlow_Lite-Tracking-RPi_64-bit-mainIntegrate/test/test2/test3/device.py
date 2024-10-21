from math import log
import time
import sys
#from psycopg2 import cursor
import cv2
import datetime


# MAX_FILE_SIZE = 62914560 # bytes
# MAX_FILE_SIZE = int(log(MAX_FILE_SIZE, 2)+1)

def get_device_config(path: str):
  
  file1 = open(path, 'r')
  
  Lines = file1.readlines()

  obj= {}

  for line in Lines:

    entries = line.split('=')

    obj[entries[0].strip()] = entries[1].strip()
    
  return obj
  
def update_status(device_id:int,cursor,status):
   
   current_time = datetime.datetime.now()
   
   time_stamp = datetime.datetime.fromtimestamp(current_time.timestamp())

   try:

    cursor.execute('''UPDATE trafficdata.devicestatus SET timestamp = %s, status = %s WHERE id = %s''', (time_stamp,status,device_id))

    return True
   
   except:
      return False

def device_init(path:str, cursor):

  time_stamp = datetime.datetime.fromtimestamp(datetime.datetime.now().timestamp())

  obj = get_device_config(path)
  
  print(obj)
  
  cursor.execute('''SELECT * FROM trafficdata.devicestatus WHERE id = %s''', (int(obj['id']),))
  
  results = cursor.fetchall()
  
  if (len(results) < 1):
    
    cursor.execute('''INSERT INTO trafficdata.devicestatus (id, status, longitude, latitude, timestamp) VALUES %s''',\
    [(int(obj['id']),True, float(obj['longitude']), float(obj['latitude']),time_stamp)])
  
  
  return int(obj['id'])

   
# def write_file(buffer, data, last_file=False):
#    # Tell `reader.py` that it needs to read x number of bytes.
#    length = len(data)
#    # We also need to tell `read.py` how many bytes it needs to read.
#    # This means that we have reached the same problem as before.
#    # To fix that issue we are always going to send the number of bytes but
#    # We are going to pad it with `0`s at the start.
#    # https://stackoverflow.com/a/339013/11106801
#    length = str(length).zfill(MAX_FILE_SIZE)
#    with open("output.txt", "w") as file:
#       file.write(length)
#    buffer.write(length.encode())

#    # Write the actual data
#    buffer.write(data)

#    # We also need to tell `read.py` that it was the last file that we send
#    # Sending `1` means that the file has ended
#    buffer.write(str(int(last_file)).encode())
#    buffer.flush()


# while True:
#     img = cv2.imread("img.jpg")
#     bimg = cv2.imencode(".jpg", img)[1]
#     # Call write_data
#     write_file(sys.stdout.buffer, bimg, last_file=False)
#     # time.sleep(1) # Don't need this
