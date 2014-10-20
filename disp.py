import os, sched, time
from threading import Timer
import proc
import sys

if os.name is 'posix':
    import curses
    def set_list_subwin(lst_win, lst):
        """
        After init the sub window and entering a address,
        to display the blocking list
        :param lst_win: the list window
        :param lst: the blocking list
        """
        lst_win.erase()
        y, x=lst_win.getmaxyx()
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLUE,curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        if curses.has_colors():
            lst_win.attrset(curses.color_pair(1))
        lst_win.insstr(0,0,'blocking list:')
        if curses.has_colors():
            lst_win.attrset(curses.color_pair(2))
        if len(lst)<=y:
            for i in range(len(lst)):
                lst_win.insstr(i+1,0, ('{index}.'+lst[i]).format(index=i+1))
        else:
            for i in range(y-1):
                lst_win.insstr(i+1,0, ('{index}.'+lst[i]).format(index=i+1))
            lst_win.insstr(y,0, '...')
        lst_win.refresh()

    def set_time_subwin(win, time, remained):
        win.erase()
        if curses.has_colors():
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
            win.attrset(curses.color_pair(4))
        if time is '\n' or time is 0:
            TIMESTR='DEFAULT TIME: {time}min'.format(time=30)
        else:
            TIMESTR='BLOCKING TIME: {time}min'.format(time=time)
        win.insstr(0,0,TIMESTR)

        REMAINSTR='Time Remaining: {remain_time}min'.format(remain_time=remained)
        win.insstr(1,0,REMAINSTR)
        win.refresh()

    def start_window(stdscr, lst, time):
        curses.echo()
        curses.cbreak()
        winY, winX=stdscr.getmaxyx()

        if curses.has_colors():
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            stdscr.attrset(curses.color_pair(3))
        ''' set welcoming '''
        WELCOME='Welcome to the ScienWebbing...Please CONCENTRATE'
        stdscr.insstr(0,(winX-len(WELCOME))/2, WELCOME)

        ''' set input field'''
        INPUT='Input site address or time: '
        stdscr.insstr(1,0,INPUT)

        ''' set annotations'''
        ANNO='(Input sites your want to block one each time, or the blocking minutes)'
        ANNO1='(Address like: xxx.xx.com Time like: 30)'
        stdscr.insstr(2,0,ANNO)
        stdscr.insstr(3,0,ANNO1)
        stdscr.refresh()

        ''' set subwin for lst '''
        #pdb.set_trace()
        list_win = stdscr.derwin(winY-4, winX/2, 4,0)
        set_list_subwin(list_win, lst)

        ''' set subwin for time '''
        time_win=stdscr.derwin(winY-4, winX/2, 4, winX/2)
        set_time_subwin(time_win,time,time)

        return (stdscr.getstr(1,len(INPUT)+1, 255),1,len(INPUT)+1, list_win, time_win)

    def preprocess_url(string):
        return string
    def keyloop(stdscr):
        lst=[]
        delay_time=30
        (str, row, col, lst_win, time_win) = start_window(stdscr, lst, delay_time)
        while str is not '':
            stdscr.move(row, col)
            stdscr.clrtoeol()
            if str.isdigit():
                delay_time=int(str)
                set_time_subwin(time_win,delay_time,delay_time)
            else:
                addr=preprocess_url(str)
                if addr is not None:
                    lst.append(addr)
                set_list_subwin(lst_win, lst)
            str=stdscr.getstr(row,col,255)

        #notify_remain_time(time_win, delay_time, delay_time)
        time_win.insstr(4,0,"Running...")
        time_win.refresh()
        for i in range(1, delay_time):
            Timer(60*i, set_time_subwin, (time_win, delay_time, delay_time-i)).start()
        Timer(60*delay_time, exit_program,(time_win,4,0 )).start()
        proc.run_proc(lst,delay_time)
        while True:
            pass


    def exit_program(win, row, col):
        if curses.has_colors():
            win.attrset(curses.color_pair(2))
        win.insstr(row,col,'Block recovered, exiting...')
        win.refresh()
        time.sleep(3)
        curses.endwin()
        sys.exit(0)

    def main(stdscr):
    #pdb.set_trace()
        keyloop(stdscr)

    curses.wrapper(main)
    #curses.endwin()
else:
    pass

