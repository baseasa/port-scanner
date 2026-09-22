import socket
from concurrent.futures import ThreadPoolExecutor

target = "x.x.x.x"

def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    result = s.connect_ex((target, port))

    if result == 0:
        print(f"port {port} is open yay!")
 

with ThreadPoolExecutor(max_workers=200) as executor:
    #ThreadPoolExecutor is a class that provides a high-level interface for asynchronously executing callables
    #max_workers : specifies the maximum number of threads that can be used to execute the given calls

    for port in range(1, 1025):
        executor.submit(scan_port, port)
        #submit() : schedules the callable (scan_port) to be executed as a separate thread
        #(scan_port, port) : run the scan_port function for this port number 
        
        
print("done!")                