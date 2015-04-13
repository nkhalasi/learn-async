import asyncio

@asyncio.coroutine
def do_work(task_name, work_queue):
    while not work_queue.empty():
        queue_item = yield from work_queue.get()
        print('{} grabbed item: {}'.format(task_name, queue_item))
        yield from asyncio.sleep(5)

def main():
    q = asyncio.Queue()
    for x in range(45):
        q.put_nowait(x)
    print(q)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    tasks = (
        asyncio.async(do_work('task1', q)),
        asyncio.async(do_work('task2', q)),
        asyncio.async(do_work('task3', q)),
        asyncio.async(do_work('task4', q))
        )

    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

if __name__ == '__main__':
    from datetime import datetime as dt
    start = dt.now()
    main()
    print(dt.now() - start)
