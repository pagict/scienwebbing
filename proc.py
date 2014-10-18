import os
from threading import Timer
TAG='TAG'
if os.name is 'nt':
        HOSTPATH='C:\Windows\System32\drivers\etc\hosts'
        TMPPATH='C:\Windows\System32\drivers\etc\hosts~'
elif os.name is 'posix':
        HOSTPATH='/etc/hosts'
        TMPPATH='/etc/tmp'
def block(lst):
        try:
                '''*********    try to open files to be read and written'''
                fd=open(HOSTPATH,'r')
                outfd=open(TMPPATH,'w+')
        except:
                print 'Please execute in admin/root!'
                exit()
        
        s=fd.readline()
        while(s):
                for addr in lst:
                        ''' ********    for each site address, add '#' to block the existing one '''
                        ''' ********    Add TAG to indicate the modification '''
                        if addr in s:       
                                s='#'+s
                                s=s[:len(s)-1]+TAG+'\n'
                                break
                outfd.write(s) # write to the temp file
                s=fd.readline()
        ''' ****  remove the hosts '''  
        filename=fd.name
        fd.close()
        os.remove(filename)

        ''' ****  add redirection to the localhost '''
        for addr in lst:
                s='127.0.0.1 '+addr+'#'+TAG+' \n'
                outfd.write(s)
        outfd.close()
        
        os.rename(TMPPATH,HOSTPATH) # rename to hosts
                        
def recovery():
        try:
                outfd=open(TMPPATH,'w+')
                fd=open(HOSTPATH,'r')
        except:
                print 'Please execute in admin/root!'
                exit()
                
        s=fd.readline()
        while(s):
                if '#'+TAG not in s : #
                        ''' **************   for the existing ones , remove the # and the TAG '''
                        ''' *********     For the new added blocking ones, directly ignored '''
                        if TAG in s:
                                s=s[1:len(s)-4]+'\n'
                        outfd.write(s)
                s=fd.readline()
        ''' ********* remove the hosts '''
        filename=fd.name
        fd.close()
        os.remove(filename)
        ''' ********* rename the temp to hosts '''
        outfd.close()
        os.rename(TMPPATH, HOSTPATH)
        
def run_proc(lst, delay_time):

    block(lst)

    Timer(60*delay_time, recovery, ()).start()
    '''
    t=sched.scheduler(time.time, time.sleep)
    t.enter(delay_time, 5, recovery,())
    t.run()'''
