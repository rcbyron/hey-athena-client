Installation Notes
==================
Use the "Manual (GitHub) Installation" to debug installation issues.

Ubuntu/Raspberry Pi/Linux
-------------------------
-  ``sudo apt-get update -y``
-  ``sudo apt-get install -y python3 python3-dev python3-pip build-essential swig git portaudio19-dev python3-pyaudio flac``  
-  ``sudo pip3 install pocketsphinx HeyAthena``  

-  Install AVBin 10:

   -  http://avbin.github.io/AVbin/Download.html
   -  ``chmod +x ./install-avbin-linux-XXX-XX-v10``
   -  ``sudo ./install-avbin-linux-XXX-XX-v10``
    
-  ``sudo python3``
-  ``>>> from athena import __main__``

Windows
-------

-  Install SWIG (can be removed after installing):

   -  http://www.swig.org/download.html
   -  Download swigwin-3.X.X and place swig.exe in your environment PATH

-  ``python -m pip install pyaudio``

-  Install AVBin 10:

   -  http://avbin.github.io/AVbin/Download.html
   -  Verify that the avbin.dll or avbin64.dll was placed in SysWOW64 not System32

-  ``pip3 install HeyAthena``
-  Now open up Python 3 and run ``>>> from athena import __main__``

Mac OS X
--------
- Using Homebrew package manager, type ``brew install swig``
- ``brew install portaudio`` ``pip install pyaudio```
-  Install AVBin 10:

   -  http://avbin.github.io/AVbin/Download.html
-  ``pip3 install HeyAthena``
-  Now open up Python 3 and run ``>>> from athena import __main__``

Manual (GitHub) Installation
----------------------------
-  Install SWIG, PyAudio, and AVBin using the directions above (depending on your operating system)
-  ``pip3 install pocketsphinx pyaudio SpeechRecognition pyglet gTTS pyyaml wolframalpha selenium``
-  Clone or download the ``hey-athena-client`` repository
-  Add ``C:\path\to\hey-athena-client`` to your ``PYTHONPATH`` system or
   user environment variable

   -  Eclipse (PyDev) has an option for this while importing the project
      from Git

-  ``cd hey-athena-client-master\client``
-  ``python __main__.py``

Okay I think I've installed everything. Now what?
-------------------------------------------------

-  If all goes well, create a user, say "Athena", and ask her a question!
-  Otherwise post an issue describing the error to the GitHub repository linked above
-  You can add modules/edit the client in Python's site-packages/athena
   folder
-  Try writing your own module using the directions below!