import time
import zmq
import db_logger

class db_logger_zmq(db_logger.db_logger):
	
	def __init__(self, address):
		super(db_logger_zmq, self).__init__()
		self.address = address

	def connect(self):
		self.context = zmq.Context()
		self.subscriber = self.context.socket(zmq.SUB)
        
		try:
			self.subscriber.connect(self.address)
		except zmq.ZMQError as error:
			print("Error during connecting to ZMQ proxy:", error)


	def subscribe(self, l):
		for i in l:
			self.subscriber.setsockopt(zmq.SUBSCRIBE, i.encode("utf-8"))	

	def listen(self):
		try:
			while True:
				[address, contents] = self.subscriber.recv_multipart()
				# logger.log_json(contents)
				print("Recieved")
		except KeyboardInterrupt:
			print("\nStopped by user")
		finally:
			self.close()

	def close(self):
		self.subscriber.close()
		self.context.term()
		self.close_database()
