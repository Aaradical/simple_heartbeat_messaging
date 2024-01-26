import socket
import datetime
import time


# IP configuration for service
address = ('127.0.0.1', 8000)

# Establishes socket connection, udp was used as
udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udpSocket.bind(address)

# Throws an exception if a timeout occurs
udpSocket.settimeout(3)
try:
    # Receives data from other service, and also sends data to other service
    while True:
        data, sourceAddress = udpSocket.recvfrom(128)
        received = str(datetime.datetime.now())
        print("Recv: ", data, '|', received)
        status = "Service 1 is alive"
        udpSocket.sendto(status.encode(), sourceAddress)
        send = str(datetime.datetime.now())
        print("Send: ", status, '|', send)
        print("-----------------------------")

# Creates error log if connection to service 2 lost, contains exact datetime of when connection was lost
except socket.timeout:
    print('Service 2 is not alive, generating log file')
    print('Connection was lost at ', str(datetime.datetime.now()))
    service1ErrorLog = open("Service_1_Error_Log.txt", "w")
    service1ErrorLog.write('Lost connection to Service 2 at ' + str(datetime.datetime.now()))
    service1ErrorLog.close()
    udpSocket.close()

# Exception handling for if service is manually shutdown (for testing purposes)
except KeyboardInterrupt as ex:
    print(ex)