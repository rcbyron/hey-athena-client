Hey Athena
==========

|Travis Build| |PyPI version| |GitHub license|

Overview
--------

Your personal voice assistant. Written in Python.

"Hey Athena" is a 100% open-source, modular voice assistant framework. We aim to do everything that Siri, Cortana, and Echo can do - and more.

| **Website:** https://heyathena.com
| **Documentation:** https://heyathena.com/docs/
| **Forum:** https://heyathena.com/forum/
| **GitHub:** https://github.com/hey-athena/hey-athena-client

Usage Examples:
---------------
Say "Athena" *(wait for double beep)* then...

-  "Play some music"
-  "Text [Joe] [Wow, Hey Athena is so cool!]"
-  "Tweet [Hello world!]" (IFTTT key required)
-  "Define [artificial intelligence]"
-  "Show me pictures of [Taj Mahal]"
-  "Open facebook.com"

Write a simple "module" to control your house with your voice.
See documentation: https://heyathena.com/docs/

Don't like the name "Athena"? Change it to anything you want, like "Joe" or "Swagger Bot".

Module Ideas
------------

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

Roadmap
-------
Hey Athena is just getting started. We plan to build an **open-source community** built around a quality **voice assistance framework**. Here are some features you can expect to see in the future:

- **Bigger Community:** we are working on building a bigger open-source community
- **Passive Modules:** useful for voice/text notifications (e.g. - "You have an important unread email from Professor Valvano")
- **Module Database:** developers will be able to easily create and submit modules for other people to use
- **Machine Learning:** we are looking into libraries like `Scikit <http://scikit-learn.org/stable/>`_ to help Athena learn how to respond better
- **Natural Language Processing (NLP):** we are constantly working on improving NLP techniques with services like `wit.ai <https://wit.ai/>`_

HTTP RESTful API
----------------
We are currently developing a cloud-hosted RESTful API (JSON) service.
Users will be able to send HTTP requests and receive a voice/text JSON response.  

**Current:** ``https://heyathena.com/api?q=test``

**Future:** ``HTTP GET https://heyathena.com/api/{api_key}/q=list%20bitcoin%20price``  

**Response:** ``{"success": true, "response": "359.7", "intent": "bitcoin"}``

How can I make my own Athena?
-----------------------------

-  Download and install Hey Athena using the directions below
-  Write your own modules so Athena can respond to different commands
-  Install Hey Athena on a Raspberry Pi to turn your house into a smart-home with voice control

Installation
------------
For installation notes, please use: https://heyathena.com/docs/intro/install.html

How can I help?
---------------

-  Write modules and contribute them by submitting a pull request to this repository
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

Passive Modules
---------------

(soon-to-be implemented)

-  Passive modules will be collections of scheduled/event-triggered tasks
-  Useful for notifications (e.g. - Twitter, Facebook, GMail updates)

Athena APIs
-----------
An "Api" object is simply a separate library of functions for "Modules" to use. Athena stores a library of "Api" objects during runtime. Moreover, "Api" objects make it easy to load user configuration data at runtime. This is useful if your modules require username/password authentication (e.g. - logging into Spotify)

| **Usage example:**
| ``from athena.apis import api_lib``
| ``api_lib['your_api_handle'].your_awesome_func()``

Common Errors
-------------

| **Error:** "no module named athena"
| **Fix:** Make sure the athena project directory is in your PYTHONPATH
| 
| **Error:** "AVbin is required to decode compressed media"
| **Fix:** Pyglet needs the avbin.dll file to be installed. On Windows, sometimes the file is wrongfully placed in System32 instead of SysWOW64.
| 
| Other errors can be found by searching the issues on our GitHub page.

.. |Travis Build| image:: https://travis-ci.org/rcbyron/hey-athena-client.svg?branch=demo-branch
   :target: https://travis-ci.org/hey-athena/hey-athena-client
.. |PyPI version| image:: https://badge.fury.io/py/heyathena.svg
   :target: https://badge.fury.io/py/heyathena
.. |GitHub license| image:: https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000
   :target: https://raw.githubusercontent.com/hey-athena/hey-athena-client/connor-branch/LICENSE
