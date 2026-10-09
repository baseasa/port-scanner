import socket
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor

#ANSI color codes
GREEN = "\033[92m"
CYAN = "\033[96m"
DIM = "\033[2m"
BOLD = "\033[1m"
RED = "\033[91m"
RESET = "\033[0m"

parser = argparse.ArgumentParser(description="port scanner")
parser.add_argument("target", help="the IP address or hostname to scan")
parser.add_argument("-p", "--ports", default="1-1024",
                    help="port range, 1-1024")
args = parser.parse_args()

start_port, end_port = args.ports.split("-")
start_port = int(start_port)
end_port = int(end_port)

#resolve the hostname to an IP only once before the scan starts
#before this, every connect_ex() call could trigger its own DNS lookup
#if the name can't be resolved, stop here with a clear message instead of failing on every port
try: 
    target_ip = socket.gethostbyname(args.target)
except socket.gaierror:
    print(f"{RED}could not resolve {args.target}{RESET}")
    sys.exit(1)


def scan_port(port):
    #new in this version: this function does not print anything
    #it returns the result and the main code decides what to do with it
    #open port -> (port, service, banner) , closed port -> None

    # 'with' closes the socket automatically, even if an error happens inside
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((target_ip, port))

        if result != 0: #not 0 means the port is no open
            return None

        #find the service name
        try:
            service = socket.getservbyport(port, "tcp")
        except OSError:
            service = "unknown"

        #try to read a banner
        banner = ""
        try:
            #web servers stay silent until asked, so send a small request
            #443 is left out on purpose, it speaks TLS, plain HTTP doesn't work there
            if port in(80, 8000, 8080):
                request = f"HEAD / HTTP/1.0\r\nHost: {args.target}\t\n\r\n"
                s.sendall(request.encode())
            data = s.recv(1024)
            banner = data.decode("utf-8", errors="replace").strip()
            banner = banner.replace("\r\n", " | ") #keep it on one line
        except (socket.timeout, OSError):
            banner = ""

        return (port, service, banner)                    


ports = range(start_port, end_port + 1)

print(f"{BOLD}target:{RESET} {args.target} ({target_ip})")
print(f"{BOLD}ports:{RESET} {start_port}-{end_port}\n")

#perf_counter() is a clock made for measuring durations
#time.time() is the wall clock, it can jump if the system time changes
start_time = time.perf_counter()

with ThreadPoolExecutor(max_workers=100) as executor:
    #map() runs scan_port for every port in parallel,
    #but gives the resuly back in the same order a the ports
    #if a thread raised an error, it shows up here instead of disappearing silently
    results = list(executor.map(scan_port, ports))

elapsed = time.perf_counter() - start_time

#throw away the closed ports, keep only the open ones
open_ports = [r for r in results if r is not None]
#map() already keeps the order, but sorting makes it explicit and sage
open_ports.sort(key=lambda r: r[0])

#no print_lock anymore, only the main thread prints now, so lines can't mix
if open_ports:
    print(f"{BOLD}{'PORT':<8}{'SERVICE':<12}BANNER{RESET}")
    for port, service, banner in open_ports:
        line = f"{GREEN}{port:<8}{RESET}{CYAN}{service:<12}{RESET}"
        if banner:
            line += f"{DIM}{banner[:80]}{RESET}" #cut long banner so the table stays readable
        print(line)
else:
    print("no open ports found")

print(f"\n{len(open_ports)} open port(s) found in {elapsed:.2f} seconds")            