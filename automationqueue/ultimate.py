import os
from sys import exit, stderr
from queue import Queue
from traceback import print_exception
from bots import bot_service


def genesis():

    producer_bot_one, \
        producer_bot_two, \
        consumer, \
        failures = bot_service(Queue())

    consumer.start()
    producer_bot_one.start()
    producer_bot_two.start()

    producer_bot_one.join()
    producer_bot_two.join()
    consumer.join()

    if failures != []:
        raise Exception(failures)


if __name__ == "__main__":

    try:
        genesis()

    except Exception as e:
        print_exception(type(e), e, e.__traceback__, file=stderr)

        exit(os.EX_SOFTWARE)

    exit(os.EX_OK)
