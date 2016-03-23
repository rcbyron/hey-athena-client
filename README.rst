Hey Athena
==========

|https://travis-ci.org/hey-athena/hey-athena-client.svg?branch=connor-branch|
|PyPI version| |GitHub license|

Overview
--------

Your personal voice assistant. Written in Python 3.

"Hey Athena" is a 100% open-source, cross-platform, modular voice
assistant framework. It aims to do everything that Siri, Cortana, and
Echo can do - and more.

| **Website:** http://heyathena.com
| **Documentation:** http://heyathena.com/docs/
| **GitHub:** https://github.com/hey-athena/hey-athena-client

Usage Examples:
---------------
Say "Athena" *(wait for double beep)* then...

-  "Play some music"
-  "Text [Connor] [Wow, Hey Athena is so cool!]"
-  "Tweet [What's good Twitter homies?]" (IFTTT key
   required)
-  "Define [artificial intelligence]"
-  "Show me pictures of [Taj Mahal]"
-  "Open facebook.com"

Write a simple "module" to control your house with your voice.
See documentation: http://heyathena.com/docs/

Don't like the name "Athena"? Change it to anything you want, like "Swagger Bot" or "Home Slice".

How can I make my own Athena?
-----------------------------

-  Download and install Hey Athena using the directions below
-  Write your own modules so Athena can respond to different commands

How can I help?
---------------

-  Write modules and contribute them by submitting a pull request to
   this repository
-  Find errors and post issues
-  If you modify the framework software, submit a pull request
-  Give feedback and help us build a community!

Core Dependencies
-----------------

-  Python 3
-  Pocketsphinx (SWIG required in your PATH during installation)
-  SpeechRecognition
-  Pyglet (AVBin required)
-  PyAudio
-  gTTS
-  PyYAML
-  Selenium

Installation
------------
For installation notes, please use: http://heyathena.com/docs/intro/install.html

Active Modules
--------------

An active module is simply a collection of tasks. Tasks look for
patterns in user text input (generally through "regular expressions").
If a pattern is matched, the task executes its action. Note: module
priority is taken into account first, then task priority.

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

Module Ideas
~~~~~~~~~~~~

-  Smart-Home Control

   - `Power Outlets (Hook) <https://www.indiegogo.com/projects/hook-home-automation-on-a-budget#/>`_

   - `Thermostat (Nest) <https://github.com/jkoelker/python-nest/>`_ 
-  `IFTTT Recipes <http://ifttt.com/>`_ (use `Maker channel <https://ifttt.com/maker>`_  to trigger)
-  Grades/Homework Assignments (see `Canvas <https://canvas.instructure.com/doc/api/index.html>`_)
-  Cooking Recipe Assistant (hands-free)
-  Facebook, Twitter, GMail
-  Timer/Stopwatch
-  Calendar
-  Games (Zork, etc.)
-  Robot Movement

If you create a module, submit a pull request! We'd love to add it to
the repository. You can also email it to connor@heyathena.com

Passive Modules
---------------

(not implemented yet)

-  Passive modules will be scheduled tasks run in the background.
-  Useful for notifications (e.g. - Twitter, Facebook, GMail updates).
-  Future versions may have event triggers for modules as well.

Common Errors
-------------

| **Error:** "no module named athena"
| **Fix:** Make sure the athena project directory is in your PYTHONPATH
| 
| **Error:** "AVbin is required to decode compressed media"
| **Fix:** Pyglet needs the avbin.dll file to be installed. On Windows, sometimes the file is wrongfully placed in System32 instead of SysWOW64.
| 
| Other errors can be found by searching the issues on our GitHub page.

.. |https://travis-ci.org/hey-athena/hey-athena-client.svg?branch=connor-branch| image:: https://travis-ci.org/hey-athena/hey-athena-client.svg?branch=connor-branch
   :target: https://travis-ci.org/hey-athena/hey-athena-client
.. |PyPI version| image:: https://badge.fury.io/py/heyathena.svg
   :target: https://badge.fury.io/py/heyathena
.. |GitHub license| image:: https://img.shields.io/badge/license-GPLv3-blue.svg
   :target: https://raw.githubusercontent.com/hey-athena/hey-athena-client/connor-branch/LICENSE