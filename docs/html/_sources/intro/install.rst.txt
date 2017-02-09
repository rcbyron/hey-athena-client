Installation
============
For troubleshooting, use the "Developer (GitHub) Installation". Post any issues (with detailed error messages) to the GitHub repository.
It is highly recommended that you use a virtual environment such as "anaconda" or "miniconda" for a clean installation.

Ubuntu/Raspberry Pi/Linux
-------------------------
NOTE: Better Raspberry Pi support is coming in future versions

- For Python 2, replace python3 with python
-  ``sudo apt-get update -y``
-  ``sudo apt-get install -y python3 build-essential swig portaudio19-dev python3-pyaudio flac libpulse-dev``
-  ``sudo pip3 install HeyAthena``

-  Install AVBin 10:
   - Choose 32-bit or 64-bit depending on your OS/python version
   -  32-bit: ``wget https://github.com/downloads/AVbin/AVbin/install-avbin-linux-x86-32-v10``
   -  64-bit: ``wget wget https://github.com/downloads/AVbin/AVbin/install-avbin-linux-x86-64-v10``
   -  ``chmod +x ./install-avbin-linux-XXX-XX-v10``
   -  ``sudo ./install-avbin-linux-XXX-XX-v10``
    
-  ``python3``
-  ``>>> from athena import __main__``

Windows
-------

-  Install SWIG (can be removed after installing):

   -  http://www.swig.org/download.html
   -  Download swigwin-3.X.X and place swig.exe in your environment PATH

-  ``python -m pip install pyaudio``

-  Install AVBin 10 (for audio):

   -  http://avbin.github.io/AVbin/Download.html
   -  Verify that the avbin.dll or avbin64.dll was placed in SysWOW64 not System32

-  ``pip3 install HeyAthena``
-  Now open up Python 3 and run ``>>> from athena import __main__``

Mac OS X
--------
- Using Homebrew package manager, type ``brew install swig``
- ``brew install portaudio`` ``pip install pyaudio``
-  Install AVBin 10:

   -  http://avbin.github.io/AVbin/Download.html
-  ``pip3 install HeyAthena``
-  Now open up Python 3 and run ``>>> from athena import __main__``

Developer (GitHub) Installation
-------------------------------
-  Install SWIG, PyAudio, and AVBin using the directions above (depending on your operating system)
-  ``pip install -U pip setuptools wheel``
-  ``pip3 install -U pocketsphinx pyaudio SpeechRecognition pyglet gTTS pyyaml wolframalpha selenium``
-  Clone or download the ``hey-athena-client`` git repository
-  Add ``C:\path\to\hey-athena-client`` to your ``PYTHONPATH`` system or
   user environment variable

   -  Eclipse (PyDev) has an option for this while importing the project from Git

-  ``cd hey-athena-client-master\client``
-  ``python __main__.py``

Okay I think I've installed everything. Now what?
-------------------------------------------------

-  If all goes well, create a user, say "Athena", and ask her a question!
-  If errors occur, try debugging by importing athena unit tests:
    - ``from athena.tests import dependencies_test``
    - ``from athena.tests import input_test``
    - ``from athena.tests import mic_test``
-  Otherwise post an issue describing the error to the GitHub repository linked above
-  Continue to personalize Athena by writing your own module
-  You can add modules/edit the client in Python's site-packages/athena
   folder