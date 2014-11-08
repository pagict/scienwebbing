import os
import time


class BlockManager(object):

    def __init__(self, block_list=[], block_minutes=0):
        self.__block_list = block_list
        self.block_minutes = block_minutes
        self.__TAG = 'TAG'
        if os.name is 'nt':
            self.__HOSTPATH = 'C:\Windows\System32\drivers\etc\hosts'
            self.__TMPPATH = 'C:\Windows\System32\drivers\etc\hosts_tmp'
        elif os.name is 'posix':
            self.__HOSTPATH = '/etc/hosts'
            self.__TMPPATH = '/etc/tmp_hosts'

    def __block(self):
        try:
            '''*********    try to open files to be read and written'''
            fd = open(self.__HOSTPATH, 'r')
            tmp_fd = open(self.__TMPPATH, 'w+')
        except:
            print 'Please execute in admin/root!'
            exit()

        s = fd.readline()
        while s:
            for site in self.__block_list:
                ''' ********    for each site address, add '#' to block the existing one '''
                ''' ********    Add TAG to indicate the modification '''
                if site in s:
                    s = '#' + s
                    s = s[:len(s) - 1] + self.__TAG + '\n'
                    break
            tmp_fd.write(s)  # write to the temp file
            s = fd.readline()
        ''' ****  remove the hosts '''
        filename = fd.name
        fd.close()
        os.remove(filename)

        ''' ****  add redirection to the localhost '''
        for address in self.__block_list:
            s = '127.0.0.1 ' + address + '#' + self.__TAG + ' \n'
            tmp_fd.write(s)
        tmp_fd.close()

        os.rename(self.__TMPPATH, self.__HOSTPATH)  # rename to hosts

    def __recovery(self):
        try:
            tmp_fd = open(self.__TMPPATH, 'w+')
            fd = open(self.__HOSTPATH, 'r')
        except:
            print 'Please execute in admin/root!'
            exit()

        s = fd.readline()
        while s:
            if '#' + self.__TAG not in s:  #
                ''' **************   for the existing ones , remove the # and the TAG '''
                ''' *********     For the new added blocking ones, directly ignored '''
                if self.__TAG in s:
                    s = s[1:len(s) - 4] + '\n'
                tmp_fd.write(s)
            s = fd.readline()
        ''' ********* remove the hosts '''
        filename = fd.name
        fd.close()
        os.remove(filename)
        ''' ********* rename the temp to hosts '''
        tmp_fd.close()
        os.rename(self.__TMPPATH, self.__HOSTPATH)

    def run(self):
        os.setsid()
        self.__block()
        time.sleep(60 * self.block_minutes)
        self.__recovery()

    def add_site(self, site):
        if type(site) is str:
            self.__block_list.append(site)