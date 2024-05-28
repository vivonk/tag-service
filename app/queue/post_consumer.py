import boto3
import app.config as config
from app.queue.common import SignalHandler
from app.processor import tag_request_processor
import warnings
import urllib3
import threading
from loguru import logger

logger = logger.bind(name="tag_request_consumer")
# Suppress the InsecureRequestWarning for all urllib3 connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Suppress the InsecureRequestWarning for all warnings
warnings.filterwarnings('ignore', 'Unverified HTTPS request')

sqs = boto3.resource("sqs")
queue = sqs.get_queue_by_name(QueueName=config.tag_request_queue)
dlq = sqs.get_queue_by_name(QueueName=config.tag_request_dlq)
signal_handler = SignalHandler()


def process_dlq():
	while not signal_handler.received_signal:
		messages = dlq.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20, )
		for message in messages:
			try:
				tag_request_processor.process(message.body)
			except Exception as e:
				logger.error(f"exception while processing message: {e}")
				continue
			message.delete()


def process_queue():
	while not signal_handler.received_signal:
		messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5, )
		for message in messages:
			try:
				tag_request_processor.process(message.body)
			except Exception as e:
				logger.error(f"exception while processing message: {e}")
				continue
			message.delete()


if __name__ == "__main__":
	logger.info("Starting up tag request consumer")
	# run both process methods in threads and wait for threads
	# to finish before exiting
	queue_thread = threading.Thread(target=process_queue)
	dlq_thread = threading.Thread(target=process_dlq)
	queue_thread.start()
	dlq_thread.start()
	queue_thread.join()
	dlq_thread.join()
	logger.info("Shutting down tag request consumer")