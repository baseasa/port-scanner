import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description = "simple port scanner")
'''
argparse.ArgumentParser() : creates a new ArgumentParser object that will hold all the information necessary to parse the command line into Python data types
description : a description of what the program does, which will be displayed when the user runs the program with the --help option
'''
parser.add_argument("target", help = "the IP address or hostname to scan")
#add_argument() : defines a new command-line argument that the program will accept
args = parser.parse_args()
#parse_args() : parses the command line arguments and returns an object containing the values of the arguments

target = args.target
#target : the IP address or hostname to scan which is obtained from the command-line arguments

def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((target, port))
        if result == 0:
            print(f"port {port} is open yay!")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=200) as executor:
        for port in range(1, 1025):
            executor.submit(scan_port, port)

    print("done!")        