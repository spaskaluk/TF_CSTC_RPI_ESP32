
import scapy.all as scapy
import socket
import netifaces
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from io import BytesIO
from datetime import datetime 
from time import sleep
from os import listdir


PORT = 5005
BUFFER_SIZE = 4096
JPEG_TERMINATOR = b'\xff\xd9'
JPEG_PREFIX = b'\xff\xd8'

def get_default_gateway_ip():
    gateways = netifaces.gateways()
    default_gateway = gateways['default'][netifaces.AF_INET][0]
    return default_gateway

  
def scan(ip):
    arp_req_frame = scapy.ARP(pdst = ip)

    broadcast_ether_frame = scapy.Ether(dst = "ff:ff:ff:ff:ff:ff")
    
    broadcast_ether_arp_req_frame = broadcast_ether_frame / arp_req_frame

    answered_list = scapy.srp(broadcast_ether_arp_req_frame, timeout = 1, verbose = False)[0]
    result = []
    for i in range(0,len(answered_list)):
        client_dict = {"ip" : answered_list[i][1].psrc, "mac" : answered_list[i][1].hwsrc}
        result.append(client_dict)

    return result
  
def display_result(result):
    print("-----------------------------------\nIP Address\tMAC Address\n-----------------------------------")
    for i in result:
        print("{}\t{}".format(i["ip"], i["mac"] ))
    print(result)

def find_esp_and_connect(list_ips):
    for ips in list_ips:
        print("Attempting to get ACK from "+ips["ip"])
        s = socket.socket()
        s.settimeout(5.0)
        try:
            s.connect((ips["ip"], PORT))
        except socket.timeout as e:
            print(e, ": no connections after 5 seconds...")
            print("Moving on to the next IP")
            print("---------------------------------------")
            s.close()
            # Go to the next connection
            continue
        except ConnectionRefusedError as e:
            print("Not ESP32-CAM")
            s.close()
            continue

        res = s.recv(BUFFER_SIZE)
        if (res[:2] == JPEG_PREFIX):
            s.settimeout(None)
            print("Connection Established with ESP32-CAM")
            frame = res
            while True:
                data = s.recv(BUFFER_SIZE)
                frame += data
                if data[-2:] == JPEG_TERMINATOR:
                    img = BytesIO(frame)
                    # fn = str(datetime.now()).replace(" ","-").replace(":","-")
                    # While there is 1 file in the directory, wait. Wait for model code to remove the file and go to the next one.
                    while(len(listdir("../../current_imgs/")) == 1):
                        pass
                    Image.open(img).save("../../current_imgs/file.jpeg", "JPEG")
                    frame = bytes()
        s.close()


def main():
    default_gateway_ip = get_default_gateway_ip()
    # display_result(scanned_output)
    d = scan(default_gateway_ip+"/24")
    while(len(d) == 0): 
        print("No connections found, scanning again.")  
        sleep(5)
        d = scan(default_gateway_ip+"/24")
        print(d)
    
    find_esp_and_connect(d)


if __name__ == "__main__":   
    while True:
        main()




