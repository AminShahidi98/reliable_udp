# reliable_udp
A reliable implementation of udp protocol using ACK and NACK. Program consists of two main functions. receiveUDPMessage() and sendUDPMessage().
Two threads are created for each 
```python
receive = threading.Thread(target = recieveUDPMessage)
send = threading.Thread(target = sendUDPMessage)

receive.start()
send.start()
```
Sender asks user for a message to send then encodes the message and send it. if after 5 seconds no messages are received then closes the socket. if the received message is not '200-ok' then the message is not sent or the received ACK is corupted, so send the message again.
```python
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
```
On the reciever side if a message is received, send '200-ok' as a ACK to the sender of message.
 ```python
 #Show message details to user
 print('----NEW MESSAGE!---------------------------------------------')
 print(clientMsg)
 print(clientIP)
 print('-------------------------------------------------------------\nEnter your message tosend:\n')
        
 #Sending a reply to client
 if message != b'200-OK':
     UDPReceiverSocket.sendto(str.encode('200-OK'), addressPair)
 ```
 Although we call one thread sender and the other receiver, both can send messages to each other. but only sender thread can start the conversation and only the reciever thread provides ACK for the messages it recieves.
