import os
from sys import exit, stderr
from queue import Queue
from traceback import print_exception
from bots import bot_service


def genesis():

    params = bot_service(Queue())

    params["consumer"].start()
    params["bot_one"].start()
    params["bot_two"].start()

    params["bot_one"].join()
    params["bot_two"].join()
    params["consumer"].join()

    if params["failures"] != []:
        raise Exception(params["failures"])


if __name__ == "__main__":

    try:
        genesis()

    except Exception as e:
        print_exception(type(e), e, e.__traceback__, file=stderr)

        exit(os.EX_SOFTWARE)

    exit(os.EX_OK)
