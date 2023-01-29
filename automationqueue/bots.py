import threading
import logging
from time import sleep
from random import random
from queue import Queue, Empty
from sqlite3 import Connection, connect
from typing import Callable, List, TypedDict, Optional
from infra.querys.bot_query import capture_bot_query, intersection_bot_query

class CrawlerService(TypedDict):
    capture_bot: threading.Thread
    intersection_bot: threading.Thread
    consumer: threading.Thread
    failures: list[str]


def crawler(db_file: str, queue: Queue) -> CrawlerService:

    failures: List[str] = []

    def get_code() -> float: return random()

    def producer_capture_bot(queue: Queue, code: float):

        label = "producer_capture_bot"

        logging.info(f'{label}: running...')

        queue.put({'CAPTURE_BOT': [code]})

        sleep(code)

        queue.put(None)

        logging.info(f'{label}: done')

        queue.task_done()

    def producer_intersection_bot(queue: Queue, code: float):

        label = "producer_intersection_bot"

        logging.info(f'{label}: running...')

        queue.put({'INTERSECTION_BOT': [code]})

        sleep(code)

        queue.put(None)

        logging.info(f'{label}: done')

        queue.task_done()

    def consumer(queue: Queue, code: float, db_file: str):

        conn: Optional[Connection] = None
        
        label = "Consumer"

        logging.info(f'{label}: running...')
        
        item: Optional[dict] = None
        
        while True:

            try:

                item = queue.get(block=False)
                
                if item is None:
                    break

                logging.info(f'Message:{item}')

                con = connect(db_file)
                
                cur = con.cursor()

                for key, value in item.items():

                    if 'CAPTURE_BOT' == key:
                        print("CAPTURE_BOT")
                        pass
                        # cur.execute(capture_bot_query(), value)
                        
                    if 'INTERSECTION_BOT' == key:
                        print("INTERSECTION_BOT")
                        pass
                        # cur.execute(intersection_bot_query(), value)
                        
                con.commit()

            except Empty:
                logging.info(f'{label}: No messages, waiting...')
                sleep(code)
                continue
            
            else:
                print("qsize:=", queue.qsize())
                queue.task_done()
                logging.info(f'{label}: done')

            finally:
                if conn:
                    conn.close()
                    logging.info(f'{label}: Close the connection manually')



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

