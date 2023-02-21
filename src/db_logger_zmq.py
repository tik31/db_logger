import zmq
import db_logger

logger = db_logger.db_logger()
logger.open_database("../db/test.db")
# del(db_logger)

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
		logger.log_json(contents)
		# print(f"[{address}] {contents}")
except KeyboardInterrupt:
	print("\nStopped by user")
finally:
	subscriber.close()
	context.term()
	del(logger)