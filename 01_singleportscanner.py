import socket

target = "x.x.x.x"
port = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1) 
'''
socket.socket(..) creates a new socket : socket is an endpoint for sending or receiving data across a computer network
socket.AF_INET is the address family for IPv4
socket.SOCK_STREAM is the socket type for TCP
'''

result = s.connect_ex((target, port))
'''
connect_ex() is a method that attempts to connect to the specified address and port, 
it returns 0 if the connection is successful (port is open), or an error code if the 
connection fails (port is closed)    
'''

if result == 0:
    print(f"port {port} is open yay!")
else:
    print(f"port {port} is closed")

s.close()