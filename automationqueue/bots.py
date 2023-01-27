import threading
import logging
from enum import Enum
from time import sleep
from random import random
from queue import Queue, Empty
from sqlite3 import Connection, connect
from typing import Callable, List, TypedDict, Optional

class CrawlerService(TypedDict):
    capture_bot: threading.Thread
    intersection_bot: threading.Thread
    consumer: threading.Thread
    failures: list[str]


class ThreadsBots(Enum):
    CAPTURE_BOT = 1
    INTERSECTION_BOT = 2
    CONSUMER = 3


def crawler(db_file: str, queue: Queue) -> CrawlerService:

    failures: List[str] = []

    def get_code() -> float: return random()

    def producer_capture_bot(queue: Queue, code: float):

        label = "producer_capture_bot"

        logging.info(f'{label}: running...')

        queue.put({ThreadsBots.CAPTURE_BOT: [code]})

        sleep(code)

        queue.put(None)

        logging.info(f'{label}: done')

    def producer_intersection_bot(queue: Queue, code: float):

        label = "producer_intersection_bot"

        logging.info(f'{label}: running...')

        queue.put({label: [code]})

        sleep(code)

        queue.put(None)

        logging.info(f'{label}: done')

    def consumer(queue: Queue, code: float, db_file: str):

        conn: Optional[Connection] = None
        
        label = "Consumer"

        logging.info(f'{label}: running...')

        while True:

            try:
                item = queue.get(block=False)

                # con = connect(db_file)
                
                # cur = con.cursor()

                # conn.commit()

            except Empty:
                logging.info(f'{label}: No messages, waiting...')
                sleep(code)
                continue

            finally:
                if conn:
                    conn.close()

            if item is None:
                break

            logging.info(f'Message:{item}')

        queue.task_done()

        logging.info(f'{label}: done')

    def thread_producer(fn: Callable[[Queue, float], None], code: float) -> threading.Thread:
        return threading.Thread(target=fn, args=(queue, code))

    def thread_consumer(fn: Callable[[Queue, float, str], None],
                        code: float,
                        db_file: str) -> threading.Thread:

        return threading.Thread(target=fn, args=(queue, code, db_file))


    def except_hook(args) -> None:
        failures.append(f'Thread failed!!: {args.exc_value}')

    threading.excepthook = except_hook

    return {"capture_bot": thread_producer(producer_capture_bot, get_code()),
            "intersection_bot": thread_producer(producer_intersection_bot, get_code()),
            "consumer": thread_consumer(consumer, .5, db_file),
            "failures": failures}

