import socket
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor

# ANSI color codes
GREEN = "\033[92m"
CYAN = "\033[96m"
DIM = "\033[2m"
RESET = "\033[0m"

parser = argparse.ArgumentParser(description="port scanner")
parser.add_argument("target", help = "the IP address or hostname to scan")
parser.add_argument("-p", "--ports", default="1-1024",
                    help = "port range, 1-1024")
args = parser.parse_args()

target = args.target

start_port, end_port = args.ports.split("-")
start_port = int(start_port)
end_port = int(end_port)

#a lock so only one thread prints at a time (keeps output lines from mixing)
print_lock = threading.Lock()

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))

    if result == 0: #0 means the port is open
        #find the service name 
        try: 
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "unknown"

        #try to read a banner (the service's greeting/version)
        banner = ""
        try:
            #web servers stay silent until asked, so send a small request first
            if port in (80, 8080, 443):
                request = f"HEAD / HTTP/1.0\r\nHost: {target}\r\n\r\n"
                s.sendall(request.encode())
            data = s.recv(1024)
            banner = data.decode("utf-8", errors="replace").strip() 
            banner = banner.replace("\r\n", " | ") #keep it on one line
        except (socket.timeout, OSError):
            banner = ""             

        #only one thread prints at a time, so colored lines never mix
        with print_lock:
            line = f"{GREEN}port {port} is open{RESET} ({CYAN}{service}{RESET})"
            if banner:
                line += f" {DIM} -> {banner}{RESET}"
            print(line) 

    s.close()

with ThreadPoolExecutor (max_workers=100) as executor:
    for port in range(start_port,end_port + 1):
        executor.submit(scan_port, port)

print("done!")