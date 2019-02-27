from my_states import Receiver


class FSM:
	"""
	A simple state machine to cycle through
	our states.
	"""
	def __init__(self):
		""" Initialize The Components. """
		# Start With A Default State
		self.state = Receiver()
		
	def on_event(self, event):
		"""
		Incoming events are delegated to the given states which then
		handle the event. The result is then assigned as the new state.
		"""
		# The Next State Is The Result Of on_event
		self.state = self.state.on_event(event)
