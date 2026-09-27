import socket
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(description="port scanner")
parser.add_argument("target", help="the IP address or hostname to scan")

parser.add_argument("-p", "--ports", default="1-1024",
                    help="port range, 1-1024, default = 1 - 1024")

args = parser.parse_args()
target = args.target

start_port, end_port = args.ports.split("-")
start_port = int(start_port)
end_port = int(end_port)

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    result = s.connect_ex((target, port))

    if result == 0: #0 means the connection succeedded -> port is open
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

            data = s.recv(1024) #read up to 1024 bytes the service sends
            banner = data.decode("utf-8", errors="replace").strip() #recv gives raw bytes, so decode them into readable text
        except (socket.timeout, OSError):
            banner = "" #no banner came, that's fine

        if banner:
            print(f"port {port} is open ({service}) -> {banner}")
        else:
            print(f"port {port} is open ({service})")
    s.close()           

with ThreadPoolExecutor (max_workers=100) as executor:
    for port in range(start_port, end_port + 1):
        executor.submit(scan_port, port)

print("done!")                  
