import socket
import time
import system
import os
import hashlib
import random

class Reciever:

    def __init__(win_size, timeout, num_packets,filename):
        self.w = win_size
        self.t = timeout
        self.n = num_packets
        self.rec_file = ''
        self.base = 0
        self.last_ack_packet = -1
        self.active_win_packets = 0