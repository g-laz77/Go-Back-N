import socket
import time
import system
import os
import hashlib
import random
host = ""
port = 10000
class Sender:

    def __init__(self, win_size, timeout, num_packets):
        self.w = win_size
        self.t = timeout
        self.n = num_packets
        self.filename = "sample.txt"
        self.cur_seq = 0
        self.active_spaces = self.w
        self.window = win_size * [None]
        self.soc = socket.socket()
        self.last_sent_seqnum = -1
        self.last_ack_seqnum = -1
        self.soc.connect((host,port))
        self.logf = ''

    def canAdd(self):
        if self.active_spaces == 0:
            return False
        else:
            return True

    def add(self, pack):
        self.last_sent_seqnum = self.cur_seq
        self.cur_seq + = 1
        self.window[self.w - self.active_spaces] = pack
        self.active_spaces -= 1
        self.send(pack) 

    def divide(self,data,num):
        lis = []
        while data:
            lis.append(data[:2])
            data = data[2:]
        return lis
    
    def sendmess(self,pack_list,length):
        cur_pack = 0
        while (cur_pack < length or self.last_ack_seqnum != length-1):
            while canAdd() == True and cur_pack != length - 1 :
                pack = self.makePack(cur_pack,pack_list[cur_pack]
                cur_pack = cur_pack + 1
            if self.acc_Acks() == 0:
                self.resend()
        self.soc.send("$$$$$$$")

    def run(self):
        try:
            fil = open(self.filename, 'rb')
            data = fil.read()
            pack_list = self.divide(data,256))
            f.close()
        except IOError:
            print "No such file exists"
        fname = "servlog.txt"
        self.logf = open(os.curdir + "/" + fname,"w+")
        l = len(pack_list)
        self.sendmess(pack_list,l)