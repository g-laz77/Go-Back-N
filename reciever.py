import socket
import time
import system
import os
import hashlib
import random

def check_sum(self,data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()

class Reciever:

    def __init__(win_size, timeout, filename):
        self.w = win_size
        self.completeData = ''
        self.t = timeout
        self.rec_file = ''
        self.base = 0
        self.expec_seqnum = 0
        self.last_ack_sent = -1
        self.soc = socket.socket()
        self.window = [None] * self.w
        self.active_win_packets = self.w
        self.fileclone = ''
        self.logfile = ''
        self.filepointer = 0

    def canAdd(self):             #check if a packet can be added to the send window
        if self.active_spaces == 0:
            return False
        else:
            return True
    
    def createResponse(self, seq_num):
        mess_check_sum = check_sum(self.w)
        return str(mess_check_sum) + "/////" + str(seq_num) + "/////" + str(self.w)

    def sendAcks(self, packet, counter):
        self.last_ack_sent = self.last_ack_sent + counter
        self.soc.send(packet)
        self.logfile.write(time.ctime(time.time()) + "\t" + self.logfile.write(time.ctime(time.time()) + "\t" + str(pack.split('/////')[1]) + "Sending\n")
        print "Sending ack: ", str(pack.split('/////')[1]) + "ACK\n")
    
    def remove(self, poin):
        self.window[self.window.index(poin)] = None
        self.active_win-packets += 1
        
    def add(self, packet):
        seqnum = packet.split('/////')[3]
        if self.window[seqnum % self.w] == None:
            if seqnum == self.expec_seqnum:
                self.logfile.write(time.ctime(time.time()) + "\t" + str(packet.split('/////')[1]) + "Recieve\n")
                self.active_win_packets -= 1 
                self.window[seqnum % self.w] = packet
            elif seqnum > self.expec_seqnum:
                self.logfile.write(time.ctime(time.time()) + "\t" + str(packet.split('/////')[1]) + "Recieving buffer\n")
                self.active_win_packets -= 1 
                self.window[seqnum % self.w] = packet
        
        else:
            print "In buffer!", packet.split('/////')[1]

    def appData(self)
        self.completeData += self.window[self.filepointer].split('/////')[3]
        self.filepointer += 1
        self.remove(self.filepointer - 1)
        if self.filepointer >= self.w:
            self.filepointer = 0
        
    def rMessage(self):
        while True:
            pack = self.sock.recv(2048)
            coun = 0
            if pack == '$$$$$$$':
                f = open(self.fileclone,'wb')
                f.write(self.completeData)
                f.close()
                break
            elif int(pack.split('/////')[1]) == self.expec_seqnum:
                if self.canAdd():
                    self.add(pack)
                    packet = self.createResponse(self.expec_seqnum + coun)
                    while self.window[(int(pack.split('/////')[1]) + counter)%self.w] != None:
                        self.appData()
                        coun = coun + 1
                self.sendAcks(packet, coun - 1)
                self.expected_seqnum = self.expected_seqnum + coun
            else:
                if self.canAdd():
                    self.add(pack)    

    def recieve(self, logname):
        self.logfile = open(os.curdir + '/' + logname, 'wb')
        self.rMessage()
        self.logfile.close()
