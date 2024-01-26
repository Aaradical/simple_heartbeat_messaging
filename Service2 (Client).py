import socket
import datetime
import time


# IP configuration for socket connection
address = ('127.0.0.1', 8001)

# Establishes socket connection
dataSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dataSocket.bind(address)

# Throws an exception if a timeout occurs
dataSocket.settimeout(3)
try:
    # Sends data to other service, and also receives data from it
    while True:
        status = "Service 2 is alive"
        dataSocket.sendto(status.encode(), ("127.0.0.1", 8000))
        send = str(datetime.datetime.now())
        print("Send: ", status, '|', send)
        data, sourceAddress = dataSocket.recvfrom(128)
        received = str(datetime.datetime.now())
        print("Recv: ", data, '|', received)
        print("-----------------------------")
        time.sleep(3)           # Included as a buffer to prevent constant messaging

# Creates error log if connection to service 1 lost, contains exact datetime of when connection was lost
except socket.timeout:
    print('Service 1 is not alive, generating log file')
    print('Connection was lost at ', str(datetime.datetime.now()))
    service2ErrorLog = open("Service_2_Error_Log.txt", "w")
    service2ErrorLog.write('Lost connection to Service 1 at ' + str(datetime.datetime.now()))
    service2ErrorLog.close()
    dataSocket.close()

# Error message for when service 2 (client) is started before service 1 (server)
except socket.error:
    print('Socket error; service 1 must be started before service 2')

# Exception handling for if service is manually shutdown (for testing purposes)
except KeyboardInterrupt as ex:
    print(ex)
