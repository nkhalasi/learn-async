import asyncio

def cancel_call(handle):
	handle.cancel()

def just_print_messages(loop):
	print('Just printing a new message every three seconds')
	loop.call_later(3, just_print_messages, loop)
	#handle = loop.call_later(3, just_print_messages, loop)
	#loop.call_later(1, cancel_call, handle)

def main():
	loop = asyncio.get_event_loop()
	try:
		loop.call_soon(just_print_messages, loop)
		loop.run_forever()
	finally:
		loop.close()

if __name__ == '__main__':
	main()