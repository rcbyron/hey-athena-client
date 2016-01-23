# Athena Voice
Your personal robotic assistant.

## Usage Examples
"Athena"
*(double beep)*
"Turn up"
*(plays music)*

"Athena"
*(double beep)*
"What is the price of bitcoin right now?"
*(responds with the current bitcoin price)*

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
- PyYAML

## Upcoming installation (in progress)
- Currently, pocketsphinx does not seem to install on python 3.5
- Users not using Python 3.4 and above might need to install `pip` command tool
- Download unofficial PyAudio:
    - For Python 3.4 users, download `PyAudio‑0.2.8‑cp34‑none‑win32.whl`  (tip: cp34 = Python 3.4)
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Open command prompt and switch to the download directory:
    - `cd (download directory)`
    - `pip3 install PyAudio‑0.2.8‑cp34‑none‑win32.whl`
- `pip3 install AthenaVoice`
- If all goes well, open the Python shell and run `>>> import athena` then `>>> athena.run()`

## Windows Installation (Python 3.4)
- Currently, pocketsphinx does not seem to install on python 3.5
- Users not using Python 3.4 and above might need to install `pip` command tool
- Download unofficial PyAudio:
    - For Python 3.4 users, download `PyAudio‑0.2.8‑cp34‑none‑win32.whl`  (tip: cp34 = Python 3.4)
    - http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Open command prompt and switch to the download directory:
    - `cd (download directory)`
    - `pip3 install PyAudio‑0.2.8‑cp34‑none‑win32.whl`
    - `pip3 install pocketsphinx SpeechRecognition pyglet gTTS pyyaml wolframalpha`
- Download the `athena-voice-client` repository and extract it
- Add `C:\path\to\athena-voice-client-master` to your `PYTHONPATH` system or user environment variable
    - One easy way to do this is to import the project into Eclipse (PyDev) and have it add the project to PYTHONPATH
- `cd athena-voice-client-master\client`
- If all goes well, run `brain.py`, say "Athena", and ask her a question!

## Active Modules
An active module is simply a collection of tasks. Tasks look for patterns in user text input (generally through "regular expressions"). If a pattern is matched, the task executes its action.

### Active Module Example
```python
from athena.classes.module import Module
from athena.classes.task import ActiveTask
from athena.modules.api_library import bitcoin_api

MOD_PARAMS = {
    'name': 'bitcoin', # Module name is required
    'priority': 2,     # Modules with higher priority match/execute first
}

class GetValueTask(ActiveTask):
    
    def __init__(self):
        # Give regex patterns to match text input
        super().__init__(patterns=[r'.*\b(bitcoin)\b.*'])
    
    def match(self, text):
    	 # See if the patterns match the text
        for p in self.patterns:
            if p.match(text):
                return True
        return False
    
    def action(self, text):
    	 # If a pattern matches, list the bitcoin price
        print('')
        print('~ 24 Hour Average: $'    + str(bitcoin_api.get_data('24h_avg')))
        print('~ Last Price: $'         + str(bitcoin_api.get_data('last')))
        print('')
        self.speak(str(bitcoin_api.get_data('last')))


class Bitcoin(Module):
    
    def __init__(self):
        tasks = [GetValueTask()]
        super().__init__(MOD_PARAMS, tasks)
```

## Passive Modules
(not implemented yet)

- Passive modules will be scheduled tasks run in the background.
- Useful for notifications (e.g. - Twitter, Facebook, GMail updates).
- Future versions may have event triggers for modules as well.

## Common Errors

**Error:** "no module named athena"

**Fix:** Make sure the athena project directory is in your PYTHONPATH
