import os
import logging
from sys import exit, stderr
from queue import Queue
from traceback import print_exception
from bots import crawler

def genesis():

    bots = crawler(Queue())

    bots["consumer"].start()
    bots["capture_bot"].start()
    bots["intersection_bot"].start()

    bots["capture_bot"].join()
    bots["intersection_bot"].join()
    bots["consumer"].join()

    if bots["failures"] != []:
        raise Exception(bots["failures"])


if __name__ == "__main__":

    try:
        logging.basicConfig(filename='bot.log',
                            encoding='utf-8',
                            level=logging.DEBUG)
        genesis()

    except Exception as e:
        print_exception(type(e), e, e.__traceback__, file=stderr)

        exit(os.EX_SOFTWARE)

    exit(os.EX_OK)
