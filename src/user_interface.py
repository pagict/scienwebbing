import curses
import os
import time
from threading import Timer
from multiprocessing import Process
import sys

from block_manager import BlockManager


class UserInterface(object):
    def __init__(self):
        pass

    def run(self):
        pass


class UIPosix(UserInterface):
    def __init__(self):
        super(UIPosix, self).__init__()
        self.__blocking_minutes = 30
        self.__blocking_list = []
        self.__lst_win = None
        self.__time_win = None
        self.__main_win = None

    def __set_list_win(self):
        """
        After init the sub window and entering a address,
        to display the blocking list
        """
        self.__lst_win.erase()
        y, x = self.__lst_win.getmaxyx()
        if curses.has_colors():
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        if curses.has_colors():
            self.__lst_win.attrset(curses.color_pair(1))
        self.__lst_win.insstr(0, 0, 'blocking list:')
        if curses.has_colors():
            self.__lst_win.attrset(curses.color_pair(2))

        if len(self.__blocking_list) <= y:
            for i in range(len(self.__blocking_list)):
                self.__lst_win.insstr(i+1, 0, ('{index}.'+self.__blocking_list[i]).format(index=i+1))
        else:
            for i in range(y-2):
                self.__lst_win.insstr(i+1, 0, ('{index}.'+self.__blocking_list[i]).format(index=i+1))
            self.__lst_win.insstr(y-1, 0, '--MORE--')
        self.__lst_win.refresh()

    def __set_time_win(self, remain_minutes, prompt, prompt_color=None):
        self.__time_win.erase()
        if curses.has_colors():
            curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
            self.__time_win.attrset(curses.color_pair(4))
        time_str = 'BLOCKING TIME: {time}min'.format(time=self.__blocking_minutes)
        self.__time_win.insstr(0, 0, time_str)
        remain_str = 'Time Remaining: {remain_time}min'.format(remain_time=remain_minutes)
        self.__time_win.insstr(1, 0, remain_str)
        if len(prompt) > 0:
            if curses.has_colors():
                self.__time_win.attrset(prompt_color)
            self.__time_win.insstr(4, 0, prompt)
        self.__time_win.refresh()

    def __start_window(self):
        curses.echo()
        curses.cbreak()
        win_y, win_x = self.__main_win.getmaxyx()

        if curses.has_colors():
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
            self.__main_win.attrset(curses.color_pair(3))
        ''' set welcoming '''
        welcome_str = 'Welcome to the ScienWebbing...Please CONCENTRATE'
        self.__main_win.insstr(0, (win_x-len(welcome_str))/2, welcome_str)
        ''' set input field'''
        input_str = 'Input site address or time: '
        self.__main_win.insstr(1, 0, input_str)
        ''' set annotations'''
        annotation = '(Input sites your want to block one each time, or the blocking minutes)'
        annotation1 = '(Address like: xxx.xx.com Time like: 30)'
        self.__main_win.insstr(2, 0, annotation)
        self.__main_win.insstr(3, 0, annotation1)
        self.__main_win.refresh()
        ''' set subwin for lst '''
        self.__lst_win = self.__main_win.derwin(win_y-4, win_x/2, 4, 0)
        self.__set_list_win()
        ''' set subwin for time '''
        self.__time_win = self.__main_win.derwin(win_y-4, win_x/2, 4, win_x/2)
        self.__set_time_win(self.__blocking_minutes, '')
        return self.__main_win.getstr(1, len(input_str)+1, 255), 1, len(input_str)+1,

    def __preprocess_url(self, string):
        return string

    def __key_loop(self):
        string, row, col = self.__start_window()
        while string is not '':
            self.__main_win.move(row, col)
            self.__main_win.clrtoeol()
            string = string.strip()
            try:
                f = open(os.path.expanduser(string), 'r')
                line = f.readline()
                while line:
                    self.__blocking_list.append(line.strip())
                    line = f.readline()
                self.__set_list_win()
            except:
                if string.isdigit():
                    self.__blocking_minutes = int(string)
                    self.__set_time_win(self.__blocking_minutes, '')
                else:
                    url = self.__preprocess_url(string)
                    if url is not None:
                        self.__blocking_list.append(url)
                    self.__set_list_win()
            string = self.__main_win.getstr(row, col, 255)
        self.__set_time_win(self.__blocking_minutes, 'Running...', curses.color_pair(4))
        self.__time_win.refresh()
        for i in range(1, self.__blocking_minutes):
            Timer(60*i, self.__set_time_win, (self.__blocking_minutes-i, 'Running', curses.color_pair(4))).start()
        manager = BlockManager(self.__blocking_list, self.__blocking_minutes)
        p = Process(target=manager.run, args=())
        p.daemon = True
        p.start()
        p.join(self.__blocking_minutes*60)
        self.__exit_program()

    def __exit_program(self):
        self.__set_time_win(0, 'Block recovered, exiting... ', curses.color_pair(2))
        self.__time_win.refresh()
        time.sleep(3)
        curses.endwin()
        sys.exit(0)

    def run(self):
        curses.initscr()
        curses.start_color()
        curses.cbreak()
        curses.noecho()
        self.__main_win = curses.newwin(24, 80, 0, 0)
        self.__key_loop()



class UIWindows(UserInterface):
    pass