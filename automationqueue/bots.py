import threading
import logging
from time import sleep
from random import random
from queue import Queue, Empty
from typing import Callable, List, TypedDict


class CrawlerService(TypedDict):
    capture_bot: threading.Thread
    intersection_bot: threading.Thread
    consumer: threading.Thread
    failures: list[str]


def crawler(queue: Queue) -> CrawlerService:

    failures: List[str] = []

    def get_code() -> float: return random()

    def producer_capture_bot(queue: Queue, code: float):

        label = "producer_capture_bot"

        logging.info(f'{label}: running...')

        queue.put({label: [code]})

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

    def consumer(queue: Queue, code: float):

        label = "Consumer"

        logging.info(f'{label}: running...')

        while True:

            try:
                item = queue.get(block=False)
            except Empty:
                logging.info(f'{label}: No messages, waiting...')
                sleep(code)
                continue

            if item is None:
                break

            logging.info(f'Message:{item}')

        queue.task_done()

        logging.info(f'{label}: done')

    def thread_factory(fn: Callable[[Queue, float], None], code: float) -> threading.Thread:
        return threading.Thread(target=fn, args=(queue, code))

    def except_hook(args) -> None:
        failures.append(f'Thread failed!!: {args.exc_value}')

    threading.excepthook = except_hook

    return {"capture_bot": thread_factory(producer_capture_bot, get_code()),
            "intersection_bot": thread_factory(producer_intersection_bot, get_code()),
            "consumer": thread_factory(consumer, .5),
            "failures": failures}
