from math import log
import psycopg2 as pgsql
import time
import datetime
import sys

from device import *

conn = pgsql.connect(database="postgres",
                        host="psql-cstc-dev-westus-001.postgres.database.azure.com",
                        user="CSTCAdmin",
                        password="TestPassword123",
                        port="5432")


#conn = pgsql.connect(host="profolio-test-postgres.postgres.database.azure.com" ,port="5432", dbname="postgres" ,user="profolioadmin" ,password="Profolio1234" ,sslmode="require")
conn.autocommit = True

conn.set_client_encoding("utf-8")

cursor = conn.cursor()

MAX_FILE_SIZE = 4 # bytes
MAX_FILE_SIZE = int(log(MAX_FILE_SIZE, 2)+1)

object_dict = {3:'car', 4:'bike', 8:'truck', 6:'bus'}

def read(buffer, number_of_bytes):

    output = b""
    while len(output) < number_of_bytes:
        output += buffer.read(number_of_bytes - len(output))
    assert len(output) == number_of_bytes, "An error occured."
    
    return output


def read_file(buffer):
    # Read `MAX_FILE_SIZE` number of bytes and convert it to an int
    # So that we know the size of the file comming in
    
    #length = int(read(buffer, MAX_FILE_SIZE))

    # Here you can switch to a different file every time `writer.py`
    # Sends a new file
    
    # data = read(buffer, length)

    # Read a byte so that we know if it is the last file
    car_id = read(buffer, 1)

    return car_id #, (file_ended == b"1")


device_id = device_init(path='./config.txt', cursor=cursor)

current_time = datetime.datetime.now()

update_status(device_id=device_id, cursor=cursor, status=True)

try:
    for data in iter(sys.stdin.readline, b''):
        data = data.strip()
        vehicle_ID = int(data)
                
        vehicleType = object_dict[vehicle_ID]

        time = datetime.datetime.now()
        
        time_timestamp = time.timestamp()

        time_stamp = datetime.datetime.fromtimestamp(time_timestamp)

        cursor.execute('''INSERT INTO trafficdata.trafficdata (device_id, vehicletype,timestamp) VALUES %s''', [(device_id,vehicleType, time_stamp)])
        
        print("Inserted new row")

        if (time - current_time).seconds >= 59*5:

            current_time = datetime.datetime.now()

            update_status(device_id=device_id, cursor=cursor, status=True)
            
            print("Updated status of device")

except KeyboardInterrupt:
    sys.stdout.flush()



while True:

    # print("Reading file")

    data = read_file(sys.stdin.buffer)
    

    vehicle_ID = int.from_bytes(data)
    print(vehicle_ID)
"""
    vehicleType = object_dict[vehicle_ID]

    time = datetime.datetime.now()
    
    time_timestamp = time.timestamp()

    time_stamp = datetime.datetime.fromtimestamp(time_timestamp)

    cursor.execute('''INSERT INTO trafficdata.trafficdata (device_id, vehicletype,timestamp) VALUES %s''', [(device_id,vehicleType, time_stamp)])

    if (time - current_time).seconds >= 59*5:

        current_time = datetime.datetime.now()

        update_status(device_id=device_id, cursor=cursor, status=True)
"""

    # BytesIO(data).read()
    # # data, last_file = read_file(sys.stdin.buffer)
    # img_np = cv2.imdecode(np.frombuffer(BytesIO(data).read(), np.uint8),
    #                       cv2.IMREAD_UNCHANGED)
    # cv2.imshow("image", img_np)
    # cv2.waitKey(0)

    # if last_file:
    #     break;
