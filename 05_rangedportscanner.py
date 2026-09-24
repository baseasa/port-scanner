import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description = "port scanner")
parser.add_argument("target", help="the IP address or hostname to scan")

# -p makes this optional, default is used when the user doesn't pass it
parser.add_argument("-p", "--ports", default ="1-1024",
                    help ="port range, 1 - 1024 (default : 1 - 1024)")

args = parser.parse_args()

target = args.target

# args.ports is a string like "1-1024", so split it and convert to numbers
start_port, end_port = args.ports.split("-")
start_port = int(start_port)
end_port = int(end_port)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((target, port))
    if result == 0:
        print(f"port {port} is open yay!")


with ThreadPoolExecutor(max_workers=100) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, port)

print("done!")                