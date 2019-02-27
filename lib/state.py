class State:
	"""
	Defining our state object to provide utility functions
	for our individual states within our FSM.
	"""
	
	def __init__(self):
		print("Processing current state: %s" % str(self))
		
	def on_event(self, event):
		"""
		Handle events that are delegated to the specific State.
		"""
		pass
		
	def __repr__(self):
		"""
		Leverages the __str__ method to describe the State.
		"""
		return self.__str__()
		
	def __str__(self):
		"""
		Returns the name of the current State.
		"""
		return self.__class__.__name__
