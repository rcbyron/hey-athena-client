# Athena Voice
Your personal robotic assistant.

## Core Dependencies
- Python 3
- Pocketsphinx
    - Sphinxbase (packaged with pocketsphinx)
- SpeechRecognition
    - https://pypi.python.org/pypi/SpeechRecognition/#downloads
- Pyglet
    - https://bitbucket.org/pyglet/pyglet/wiki/Download
    - AVBin (library file must be seen by pyglet)
        http://avbin.github.io/AVbin/Download.html
- PyAudio
    - Linux/Mac: https://people.csail.mit.edu/hubert/pyaudio/
    - Unofficial Windows: http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- gTTS
    - requests (packaged with gTTS)

## Windows Installation (Python 3.4)
- Download unofficial PyAudio (cp34 = Python 3.4):
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Open command prompt and switch to the download directory:
    - `cd (download directory)`
    - `pip3 install PyAudio‑0.2.8‑cp34‑none‑win32.whl`
    - `pip3 install pocketsphinx SpeechRecognition pyglet gTTS wolframalpha`
- If all goes well, run `client/brain.py`, say "Athena", and ask her a question!

## Active Modules
Active modules contain a series of tasks. Each task parses user input (generally through regex) and, if it matches, responds accordingly.

### Active Module Example
```python
from client.classes.module import Module
from client.classes.task import ActiveTask
from client.tts import play_mp3

class PlaySongTask(ActiveTask):
    def __init__(self):
        super().__init__(patterns=[r'.*(\b)+turn(\s)up(\b)+.*'])
         
    def match(self, text):
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
        self.speak("Turning up...")
        play_mp3("turnup.mp3") # Searches "/media" folder if no path given
        
class Music(Module):
    def __init__(self):
        tasks = [PlaySongTask()]
        super().__init__(mod_name='music', mod_tasks=tasks, mod_priority=2)
```

## Passive Modules
(not yet implemented)
Passive modules will be scheduled tasks run in the background. Future versions may have event triggers for modules as well.
