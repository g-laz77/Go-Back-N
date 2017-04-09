import socket
import time
import system
import os
import hashlib
import random

host = ""
port = 60000


def check_sum(self, data):
    hash_md5 = hashlib.md5()
    hash_md5.update(data)
    return hash_md5.hexdigest()


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
        self.soc.connect((host, port))
        self.logfile = ''

    def canAdd(self):  # check if a packet can be added to the send window
        if self.active_spaces == 0:
            return False
        else:
            return True

    def sendPack(self, pack):  # function to send the packet through the socket
        self.sock.send(pack)
        print "Sending packet No.", int(pack.split('/////')[1])
        self.logfile.write(time.ctime(time.time()) + "\t" +
                           str(pack.split('/////')[1]) + "Sending\n")

    def add(self, pack):  # add a packet to the send window
        self.last_sent_seqnum = self.cur_seq
        self.cur_seq + = 1
        self.window[self.w - self.active_spaces] = pack
        self.active_spaces -= 1
        self.sendPack(pack)

    def resend(self):  # function to resend packet if lost
        cur_num = 0
        while cur_num < self.w - self.active_spaces:
            print "Resending: ", str(self.window[cur_num].split('/////')[1])
            self.logfile.write(time.ctime(
                time.time()) + "\t" + str(self.window[cur_num].split('/////')[1]) + "Re-sending\n")
            self.soc.send(self.window[cur_num])
            cur_num += 1

    def makePack(self, num, pac):  # Create a packet
        sequence_number = num
        file_check_sum = check_sum(pac)
        pack_size = len(pac)
        prob = random.randint(0, 100)
        packet = str(file_check_sum) + '/////' + str(sequence_number) + \
                     '/////' + str(pack_size) + '/////' + \
                                   str(pac) + '/////' + str(prob)
        return packet

    def divide(self, data, num):  # create packets from datas
        lis = []
        while data:
            lis.append(data[:num])
            data = data[num:]
        return lis

    def acc_Acks(self):  # check if all the sent packets have been ACKed
        try:
            packet = self.sock.recv(2048)
        except:
            print 'Connection lost'
            self.logfile(time.ctime(time.time()) + "\t" +
                         str(self.last_ack_seqnum + 1) + "Lost")
            return 0
        print "Recieved Ack number: ", packet.split('/////')[1]
        if int(packet.split('/////')[1]) == self.last_ack_seqnum + 1:
            self.last_ack_seqnum = packet.split('/////')[1]
            self.window.pop(0)
            self.window.append(None)
            self.active_spaces += 1
            return 1

        elif int(packet.split('/////')[1]) > self.last_ack_seqnum + 1:
            k = self.last_ack_seqnum
            while(k < int(packet.split('/////')[1])):
                self.window.pop(0)
                self.window.append(None)
                self.active_spaces += 1
                k = k + 1
            self.last_ack_seqnum = packet.split('/////')[1]
            return 1

        else:
            return 0

    def sendmess(self, pack_list, length):  # send the messages till all packets are sent
        cur_pack = 0
        while (cur_pack < length or self.last_ack_seqnum != length - 1):
            while canAdd() == True and cur_pack != length - 1:
                pack = self.makePack(cur_pack, pack_list[cur_pack])
                cur_pack = cur_pack + 1
                self.add(pack)
            if self.acc_Acks() == 0:
                self.resend()
        self.soc.send("$$$$$$$")

    def run(self):  # run this to send packets from the file
        try:
            fil = open(self.filename, 'rb')
            data = fil.read()
            pack_list = self.divide(data, 256))
            f.close()
        except IOError:
            print "No such file exists"
        fname="servlog.txt"
        self.logfile=open(os.curdir + "/" + fname, "w+")
        l=len(pack_list)
        self.sendmess(pack_list, l)


if name == '__main__':
    win = raw_input("Enter window size: ")
    numpac = raw_input("Enter the number of packets: ")
    tim = raw_input("Enter the timeout: ")
    server=Sender(win, tim, numpac)
    server.soc.bind((host, port))
    server.soc.listen(5)
    conn, addr=server.soc.recv(1024)
    conn.send(str(win) + "/////" + str(tim) + "/////" + "sample.txt")
    conn.close()
    conn, addr = server.soc.recv(1024)
    server.run()
