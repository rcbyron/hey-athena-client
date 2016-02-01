Athena Voice - Your personal voice assistant.

* Requires a decent microphone
* Must install PyAudio separately
* Must install AVbin.dll separately
* Tested on Python 3.4


Usage Examples:
>>> import athena.brain

"Athena"
*(double beep)*
"What's the weather like at DFW?"
*(responds with weather info)*

"Athena"
*(double beep)*
"What is the price of bitcoin right now?"
*(responds with the current bitcoin price)*

Common Errors:
Error: "no module named athena"
Fix: Make sure the athena project directory is in your PYTHONPATH

Error: "AVbin is required to decode compressed media"
Fix: Pyglet needs the avbin.dll file to be installed. On Windows, sometimes the file is wrongfully placed in System32 instead of SysWOW64.
