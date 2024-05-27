from signal import SIGINT, SIGTERM, signal
from loguru import logger

logger = logger.bind(name="signal_handler")

class SignalHandler:
	def __init__(self):
		self.received_signal = False
		signal(SIGINT, self._signal_handler)
		signal(SIGTERM, self._signal_handler)
	
	def _signal_handler(self, signal, frame):
		logger.info(f"handling signal {signal}, exiting gracefully")
		self.received_signal = True
