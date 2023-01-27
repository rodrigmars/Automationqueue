import threading
from time import sleep
from random import random
from queue import Queue, Empty
from typing import Callable, List, TypedDict

class BotsService(TypedDict):
    bot_one: threading.Thread
    bot_two: threading.Thread
    consumer: threading.Thread
    failures: list[str]

def bots_service(queue: Queue) -> BotsService:

    failures: List[str] = []

    def get_code() -> float: return random()

    def producer_bot_one(queue: Queue, code: float):

        print('producer_bot_one: running...')

        queue.put({"producer_bot_one": [code]})

        sleep(code)

        queue.put(None)

        print('producer_bot_one: done')

    def producer_bot_two(queue: Queue, code: float):

        print('producer_bot_two: running...')

        queue.put({"producer_bot_two": [code]})

        sleep(code)

        queue.put(None)

        print('producer_bot_two: done')

    def consumer(queue: Queue, code: float):

        print('Consumer: running...')

        while True:

            try:
                item = queue.get(block=False)
            except Empty:
                print('Producer: No messages, waiting...')
                sleep(code)
                continue
            
            if item is None:
                break

            print(f'Message:{item}')
   
        queue.task_done()

        print('Consumer: done')

    def thread_factory(fn: Callable[[Queue, float], None], code: float) -> threading.Thread:
        return threading.Thread(target=fn, args=(queue, code))

    def except_hook(args) -> None:
        failures.append(f'Thread failed!!: {args.exc_value}')

    threading.excepthook = except_hook

    return {"bot_one": thread_factory(producer_bot_one, get_code()),
                                           "bot_two": thread_factory(producer_bot_two, get_code()),
                                           "consumer": thread_factory(consumer, .5),
                                           "failures": failures}
