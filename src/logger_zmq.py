import zmq
import Logger

context = zmq.Context()
subscriber = context.socket(zmq.SUB)

try:
	subscriber.connect("tcp://localhost:5559")
except zmq.ZMQError as error:
	print("Error during connecting to ZMQ proxy:", error)
	
subscriber.setsockopt(zmq.SUBSCRIBE, b"DB_LOGGER")

try:
	while True:
		[address, contents] = subscriber.recv_multipart()
		print(f"[{address}] {contents}")
except KeyboardInterrupt:
	print("\nStopped by user")
finally:
	subscriber.close()
	context.term()