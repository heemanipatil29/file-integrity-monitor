import socket

website = input("Enter website: ")

try:
    ip = socket.gethostbyname(website)
    print("IP Address:", ip)
except socket.gaierror:
    print("Invalid website!")

