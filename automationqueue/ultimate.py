
import os
import logging
from sys import exit, stderr
from queue import Queue
from bots import crawler
from traceback import print_exception
from infra.querys.tables import create_tables
from dotenv import dotenv_values


def genesis(db_file: str) -> None:
    
    bots = crawler(db_file, queue := Queue())

    bots["consumer"].start()
    bots["capture_bot"].start()
    bots["intersection_bot"].start()

    bots["capture_bot"].join()
    bots["intersection_bot"].join()
    bots["consumer"].join()
    queue.join()

    if [] != (failures := bots["failures"]):
        raise Exception(failures)


if __name__ == "__main__":

    failed: int = 0

    try:

        logging.basicConfig(filename='bot.log',
                            encoding='utf-8',
                            level=logging.DEBUG)

        config = dotenv_values(".env")

        if not (db_file := config.get("DB_FILE")) is None:
            if not (err := create_tables(db_file)) is None:
                raise Exception(err)
            genesis(db_file)

        else:
            raise Exception("Missing db_file value")

    except Exception as e:

        print_exception(type(e), e, e.__traceback__, file=stderr)

        failed = 1

    exit(os.EX_OK if failed < 1 else os.EX_SOFTWARE)
