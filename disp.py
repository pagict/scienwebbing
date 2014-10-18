import os
import pdb

if os.name is 'posix':
    import curses
    def set_list_subwin(lst_win, lst):
        y, x=lst_win.getmaxyx()

    def start_window(stdscr, lst, time):
        curses.echo()
        curses.cbreak()
        winY, winX=stdscr.getmaxyx()
        ''' set welcoming '''
        WELCOME='Welcome to the ScienWebbing...Please CONCENTRATE'
        stdscr.insstr(0,(winX-len(WELCOME))/2, WELCOME)
        ''' set input field'''
        INPUT='Input site address or time: '
        stdscr.insstr(1,0,INPUT)
        s=stdscr.getstr(1,len(INPUT)+1, 255)
        ''' set annotations'''
        ANNO='(Input sites your want to block one each time, or the blocking minutes)'
        ANNO1='(Address like: xxx.xx.com Time like: 30)'
        stdscr.insstr(2,0,ANNO)
        stdscr.insstr(3,0,ANNO1)
        ''' set subwin for lst '''
        list_win
        ''' set subwin for time '''
        return s
    def keyloop(stdscr):
        s = start_window(stdscr, {}, 30)

        while s is not '\n':


    def main(stdscr):
	#pdb.set_trace()
        keyloop(stdscr)

    curses.wrapper(main)
else:
    pass

