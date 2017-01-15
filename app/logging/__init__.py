from colorama import Fore

DEBUG = 4
INFO = 3
WARN = 2
ERROR = 1
NONE = 0

LOG_LEVEL = 5


def info(any, color=Fore.CYAN):
    if LOG_LEVEL >= INFO:
        print(color + any + Fore.RESET)


def warn(any, color=Fore.CYAN):
    if LOG_LEVEL >= WARN:
        print(color + any + Fore.RESET)
