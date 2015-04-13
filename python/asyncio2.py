import asyncio
from datetime import datetime as dt

def timeit(f):
    def new_f(*args, **kwargs):
        start = dt.now()
        r = f(*args, **kwargs)
        print('{} completed in {} seconds'.format(f, dt.now() - start))
        return r
    new_f.__name__ = f.__name__
    return new_f

@timeit
@asyncio.coroutine
def my_coroutine(future, task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1} seconds.'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    future.set_result('{} is finished'.format(task_name))

def got_result(future):
    print(future.result())

loop = asyncio.get_event_loop()
future1 = asyncio.Future()
future2 = asyncio.Future()
future3 = asyncio.Future()

tasks = (
    asyncio.async(my_coroutine(future1, 'Task1', 4)),
    asyncio.async(my_coroutine(future2, 'Task2', 3)),
    asyncio.async(my_coroutine(future3, 'Task3', 2))
    )

future1.add_done_callback(got_result)
future2.add_done_callback(got_result)
future3.add_done_callback(got_result)

loop.run_until_complete(
    asyncio.wait(tasks)
)
loop.close()
