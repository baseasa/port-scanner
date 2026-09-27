import socket 
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="port scanner")
parser.add_argument("target", help="the IP address or hostname to scan")

parser.add_argument("-p", "--ports", default="1-1024",
                    help="port range, 1 - 1024, default = 1-1024")

args = parser.parse_args()

target = args.target

start_port, end_port = args.ports.split("-")
start_port = int(start_port)
end_port = int(end_port)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))
    if result == 0:
        #try to find the service name for this port
        try: #attempt to do this - try to find the service name
            service = socket.getservbyport(port, "tcp")
        except OSError: #if an error happens (the name can't be found) - don't crash, do this instead - set the service name to "unknown"
            service = "unknown"
        print(f"port {port} is open ({service})")
    s.close()            

with ThreadPoolExecutor (max_workers=100) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, port)

print("done!")        


