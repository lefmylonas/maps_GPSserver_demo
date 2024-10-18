#!/usr/bin/python3
import socket
from time import time, sleep
from sys import stdout
from argparse import ArgumentParser

def parsing_inputs():
    parser = ArgumentParser()
    parser.add_argument('--ip', type=str, default="127.0.0.1")
    parser.add_argument('--port', type=int, default=65432)
    args = parser.parse_args()
    return args.ip, args.port


def loading_animation(duration):
    spinner = ['|', '/', '-', '\\']
    start_time = time()
    idx = 0

    while time() - start_time < duration:
        stdout.write(f'\rSending GPS data {spinner[idx]}')
        stdout.flush()
        idx = (idx + 1) % len(spinner)
        sleep(0.2)

def parse_gps_data(data):
    firstSplit= data.split(':')
    return firstSplit[1]

def start_client(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Client broadcasting GPS data to {host}:{port}")
        lat = 51.505
        lon = -0.09
        
        while True:
            message = 'no_input'
            lat = lat + 0.01
            lon = lon + 0.01

            rpiResponse = " +CGNSINF: 1,1,20241006122501.000," + str(lat) + "," + str(lon) +",72.903,0.00,53.2,2,,0.7,1.1,0.8,,13,15,,,31,,"
            print("\n",rpiResponse)

            message = parse_gps_data(rpiResponse)
            if message == 'no_input':
                print("No input data")
            elif message == ',,,,,,':
                print("Error on GPS data")
            else:
                s.sendall(message.encode())
                loading_animation(2)

if __name__ == "__main__":
    serverIP, serverPort = parsing_inputs()
    start_client(serverIP, serverPort)
