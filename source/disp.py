import os
import time
from threading import Timer
from multiprocessing import Process
import sys

import proc


def main():
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
            y, x = lst_win.getmaxyx()
            if curses.has_colors():
                curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
                curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            if curses.has_colors():
                lst_win.attrset(curses.color_pair(1))
            lst_win.insstr(0, 0, 'blocking list:')
            if curses.has_colors():
                lst_win.attrset(curses.color_pair(2))
            #pdb.set_trace()
            if len(lst) <= y:
                for i in range(len(lst)):
                    lst_win.insstr(i+1, 0, ('{index}.'+lst[i]).format(index=i+1))
            else:
                for i in range(y-2):
                    lst_win.insstr(i+1, 0, ('{index}.'+lst[i]).format(index=i+1))
                lst_win.insstr(y-1, 0, '--MORE--')
            lst_win.refresh()

        def set_time_subwin(win, update_time, remained):
            win.erase()
            if curses.has_colors():
                curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
                win.attrset(curses.color_pair(4))
            if update_time is '\n' or update_time is 0:
                time_str = 'DEFAULT TIME: {time}min'.format(time=30)
            else:
                time_str = 'BLOCKING TIME: {time}min'.format(time=update_time)
            win.insstr(0, 0, time_str)

            remainstr='Time Remaining: {remain_time}min'.format(remain_time=remained)
            win.insstr(1, 0, remainstr)
            win.refresh()

        def start_window(stdscr, lst, update_time):
            curses.echo()
            curses.cbreak()
            win_y, win_x = stdscr.getmaxyx()

            if curses.has_colors():
                curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
                stdscr.attrset(curses.color_pair(3))
            ''' set welcoming '''
            welcome_str = 'Welcome to the ScienWebbing...Please CONCENTRATE'
            stdscr.insstr(0, (win_x-len(welcome_str))/2, welcome_str)

            ''' set input field'''
            input_str = 'Input site address or time: '
            stdscr.insstr(1, 0, input_str)

            ''' set annotations'''
            anno = '(Input sites your want to block one each time, or the blocking minutes)'
            anno1 = '(Address like: xxx.xx.com Time like: 30)'
            stdscr.insstr(2, 0, anno)
            stdscr.insstr(3, 0, anno1)
            stdscr.refresh()

            ''' set subwin for lst '''
            #pdb.set_trace()
            list_win = stdscr.derwin(win_y-4, win_x/2, 4, 0)
            set_list_subwin(list_win, lst)

            ''' set subwin for time '''
            time_win=stdscr.derwin(win_y-4, win_x/2, 4, win_x/2)
            set_time_subwin(time_win, update_time, update_time)

            return stdscr.getstr(1, len(input_str)+1, 255), 1, len(input_str)+1, list_win, time_win

        def preprocess_url(string):
            return string
        
        def keyloop(stdscr):
            lst = []
            delay_mins = 30
            string, row, col, lst_win, time_win = start_window(stdscr, lst, delay_mins)
            while string is not '':
                stdscr.move(row, col)
                stdscr.clrtoeol()
                string = string.strip()
                try:
                    f = open(os.path.expanduser(string), 'r')
                    line = f.readline()
                    while line:
                        lst.append(line.strip())
                        line = f.readline()
                    set_list_subwin(lst_win, lst)
                except:
                    if string.isdigit():
                        delay_mins = int(string)
                        set_time_subwin(time_win, delay_mins, delay_mins)
                    else:
                        addr = preprocess_url(string)
                        if addr is not None:
                            lst.append(addr)
                        set_list_subwin(lst_win, lst)
                string=stdscr.getstr(row, col, 255)

            #notify_remain_time(time_win, delay_time, delay_time)
            time_win.insstr(4, 0, "Running...")
            time_win.refresh()
            for i in range(1, delay_mins):
                Timer(60*i, set_time_subwin, (time_win, delay_mins, delay_mins-i)).start()
            #Timer(60*delay_time, exit_program,(time_win,4,0 )).start()
            p = Process(target=proc.run_proc, args=(lst, delay_mins, ))
            p.daemon = True
            p.start()
            #p.close()

            p.join(delay_mins*60)
            #proc.run_proc(lst,delay_time)
            exit_program(time_win, 4, 0, delay_mins)

        def exit_program(win, row, col, delay_min):
            #time.sleep(delay_min*60)
            if curses.has_colors():
                win.attrset(curses.color_pair(2))
            win.insstr(row, col, 'Block recovered, exiting...')
            win.refresh()
            time.sleep(3)
            curses.endwin()
            sys.exit(0)

        def main_disp(stdscr):
        #pdb.set_trace()
            keyloop(stdscr)

        curses.wrapper(main_disp)
        #curses.endwin()
    else:
        pass

