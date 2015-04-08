import asyncio

@asyncio.coroutine
def my_coroutine(task_name, seconds_to_sleep=3):
    print('{0} sleeping for: {1} seconds.'.format(task_name, seconds_to_sleep))
    yield from asyncio.sleep(seconds_to_sleep)
    print('{} is finished'.format(task_name))

loop = asyncio.get_event_loop()
tasks = (
    asyncio.async(my_coroutine('Task1', 4)),
    asyncio.async(my_coroutine('Task2', 3)),
    asyncio.async(my_coroutine('Task3', 2))
    )
loop.run_until_complete(
    asyncio.wait(tasks)
)
loop.close()
