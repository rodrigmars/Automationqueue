import threading
from time import sleep
from random import random
from queue import Queue, Empty
from typing import Callable

def bot_service(queue: Queue):

    failures = []

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

    def except_hook(args):
        failures.append(f'Thread failed!!: {args.exc_value}')

    threading.excepthook = except_hook

    return thread_factory(producer_bot_one, get_code()), \
        thread_factory(producer_bot_two, get_code()), \
        thread_factory(consumer, .5), failures
