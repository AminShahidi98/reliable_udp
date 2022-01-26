import socket
import threading

localIP = str(input('Enter your local IP: '))
localPort = int(input('Enter your desired port number(integer): '))

targetIP = str(input('Enter your destination IP: '))
targetPort = int(input('Enter your destination port number(integer): '))

def recieveUDPMessage():
    bufferSize  = 1024
    UDPReceiverSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPReceiverSocket.bind((localIP,localPort))
    while(True):
        messageAddressPair = UDPReceiverSocket.recvfrom(bufferSize)
        message = messageAddressPair[0]
        addressPair = messageAddressPair[1]

        clientMsg = 'Message: {}'.format(str(message))
        clientIP  = 'Client IP Address & Port: {}'.format(addressPair)
        
        #Show message details to user
        print('----NEW MESSAGE!---------------------------------------------')
        print(clientMsg)
        print(clientIP)
        print('-------------------------------------------------------------\nEnter your message to send: \n')
        
        #Sending a reply to client
        if message != b'200-OK':
            UDPReceiverSocket.sendto(str.encode('200-OK'), addressPair)

def sendUDPMessage():
    bufferSize  = 1024
    destinationAddressPair = (targetIP, targetPort)
    UDPSenderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    while(True):
        msg = str(input('Enter your message to send: \n'))
        encodedMsg = str.encode(msg)
        #Send message and recieve ack
        while(True):
            UDPSenderSocket.settimeout(5)
            try:
                UDPSenderSocket.sendto(encodedMsg, destinationAddressPair)
                msgFromDestination = UDPSenderSocket.recvfrom(bufferSize)
                msg = msgFromDestination[0]
                if msg != b'200-OK':
                    print('Failed to send. Retrying...')
                    continue
                print('----------------Successfuly received!----------------\n')
                break
            except:
                print('Failed to send. Retrying...')

receive = threading.Thread(target = recieveUDPMessage)
send = threading.Thread(target = sendUDPMessage)

receive.start()
send.start()