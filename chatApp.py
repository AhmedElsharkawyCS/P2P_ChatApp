#important  notes for all  team's members
#two sockets are necessary. The listening socket should open on a constant port, and the client port should be opened on a different (potentially dynamic) port, usually higher in the port range. As an example:
#Server sockets on port 1500, client sockets on port 1501.
#Peer1: 192.168.1.101
#Peer2: 192.168.1.102
#When peer1 connects to peer2 it looks like this: 192.168.1.101:1501 -> 192.168.1.102:1500.
#When peer2 connects to peer1 it looks like this: 192.168.1.102:1501 -> 192.168.1.101:1500.
#Listening TCP sockets are also generally run on a separate thread since they are blocking.

#################################### this is unicast chat based on P2P techniques######################################### 

import threading
import socket
#reciever client adn Inherit from threading class
class Receiver(threading.Thread):
    #set host and port number of me for receiver class
    def __init__(self,client_host_ip,client_port):
        threading.Thread.__init__(self,name="Client_Chat_Reaciever")
        self.client_host=client_host_ip
        self.client_port=client_port
    #run automatic  when call class
    def run(self):
        #initial socket
        socketObject=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ##bind the socket to a public host
        socketObject.bind((self.client_host,self.client_port))
        ##listen with maxnum 6 cleint or 6 connection with this receiver client
        #6 number is a var...
        socketObject.listen(6);
        #infinte loop during connection open to reciever multiple messages.
        while True:
            # find connection object that have data and ips of other client from socket
            connection,client_addr=socketObject.accept()
            try:
                ##store full message
                get_message=""
                
                ##infinite loop to received data during connection 
                while True:
                    #receive encoding data with 2 byte and store it
                    data=connection.recv(16)
                    #decoding to recieved data and store it in the get_message var
                    get_message=get_message+data.decode('utf-8')
                    #print recived data after close socket
                    if not data:
                        print("{}: {}".format(client_addr,get_message.strip()),"\n")
                        break
            finally:
                connection.shutdown(2)
                connection.close()
#end Reciever
########################################################################################                    
#create Sender for client && Inherit from threading class
class Sender(threading.Thread ):
      #set host and port of receiver 
      def __init__(self,to_client_host,to_client_port):
         threading.Thread.__init__(self,name="Client_Chat_Sender")
         self.to_client_host=to_client_host
         self.to_client_port=to_client_port 

      def run(self):
         ##infinite loop to send multiple message if you want
         while True:
             ##get message from the user
             get_message=input('typing...>>')
             #initial socket
             socketObject=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
             ##bind the socket to a public host
             socketObject.connect((self.to_client_host,self.to_client_port))
             #send message
             socketObject.sendall(get_message.encode('utf-8'))
             #close socket connection
             socketObject.shutdown(2)
             socketObject.close()
#end sender
##############################################################################333
#main function
def main():
    print('Please enter the following data')
########Note:- any client want send message to another client should have same address########3
    ##get ip and port from reciver cleint
    recv_ip=input('Reciever Host>>')
	##castint to int
    recv_port=int(input('Reciever Prot>>'))
    receiverObject=Receiver(recv_ip,recv_port) 
    #get info of user who that you want to send the message
    return_ip_from_sender=input("To Receiver's Host>>")
    return_port_from_sender=int(input("To Receiver's Port>>"))
    senderObject=Sender(return_ip_from_sender,return_port_from_sender)  
    ##start threading to run them parallelism 
    threads = [receiverObject.start(), senderObject.start()]


##run program
if __name__=="__main__":
     main()         
    