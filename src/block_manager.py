import os
import time
import socket
import platform
import subprocess


class BlockManager(object):

    def __init__(self, block_host=(), block_minutes=0):
        self.__block_host = list(block_host)
        self.block_minutes = block_minutes

    def run(self):
            os.setsid()
            self.__parse_host()
            self.__block()
            time.sleep(60 * self.block_minutes)
            self.__recovery()

    def add_host(self, hostname):
        if type(hostname) is str:
            self.__block_host.append(hostname)

    def __block(self):
        if 'Linux' in platform.system():
            self.__linux_block()

    def __recovery(self):
        if 'Linux' in platform.system():
            self.__linux_recovery()

    def __linux_block(self):
        for host in self.__block_address:
            cmd = 'iptables -I OUTPUT 1 -d {host} -j DROP'.format(host=host)
            subprocess.call(cmd.split(' '), stdout=subprocess.PIPE)

    def __linux_recovery(self):
        for i in range(len(self.__block_address)):
            cmd = 'iptables -D OUTPUT 1'
            subprocess.call(cmd.split(' '), stdout=subprocess.PIPE)

    def __parse_host(self):
        self.__block_address = []
        for host in self.__block_host:
            info = socket.getaddrinfo(host, None)
            for each in info:
                self.__block_address.append(each[4][0])
        self.__block_address = list(set(self.__block_address))