Hello World
===========

You can add modules/edit the client in the ".../athena/modules/active" folder.

For normal installations, the "athena" folder is stored in Python's "site-packages" folder

Here is an example module (add to ".../athena/modules/active")

.. code:: python

	"""
    File Name: hello_world.py
    Finds and returns the latest bitcoin price

    Usage Examples:
    - "What is the price of bitcoin?"
    - "How much is a bitcoin worth?"
	"""

	from athena.classes.module import Module
	from athena.classes.task import ActiveTask
	from athena.api_library import bitcoin_api

	class GetValueTask(ActiveTask):

		def __init__(self):
			# Matches any statement with the word "bitcoin"
			super().__init__(words=['bitcoin'])

		# This default match method can be overridden
		# def match(self, text):
		#    # "text" is the STT translated input string
		#    # Return True if the text matches any word or pattern
		#    return self.match_any(text)

		def action(self, text):
			 # If 'bitcoin' was found in text, speak the bitcoin price
			bitcoin_price = str(bitcoin_api.get_data('last'))
			self.speak(bitcoin_price)

	# This is a bare-minimum module
	class Bitcoin(Module):

		def __init__(self):
			tasks = [GetValueTask()]
			super().__init__('bitcoin', tasks, priority=2)

For more examples, check the ".../athena/modules/active" folder.
