import os
from sys import exit, stderr
from queue import Queue
from traceback import print_exception
from bots import bots_service


def genesis():

    bots = bots_service(Queue())

    bots["consumer"].start()
    bots["bot_one"].start()
    bots["bot_two"].start()

    bots["bot_one"].join()
    bots["bot_two"].join()
    bots["consumer"].join()

    if bots["failures"] != []:
        raise Exception(bots["failures"])


if __name__ == "__main__":

    try:
        genesis()

    except Exception as e:
        print_exception(type(e), e, e.__traceback__, file=stderr)

        exit(os.EX_SOFTWARE)

    exit(os.EX_OK)
