from user_interface import *
if __name__ == '__main__':
    if os.name is 'posix':
        from user_interface import UIPosix
        ui = UIPosix()
        ui.run()
    else:
        pass