Overview
========
"Hey Athena" is a 100% open-source, cross-platform, modular voice assistant framework written in Python 3. Our goal is to help you control things with your voice. This is accomplished by writing simple (module).py files.

| **Website:** http://heyathena.com
| **Documentation:** http://heyathena.com/docs/
| **Forum:** http://heyathena.com/forum/
| **GitHub:** https://github.com/hey-athena/hey-athena-client
| 

The Big Picture
---------------
|Graphic Overview|

Active Modules
--------------
An Active Module is simply a collection of "Active Tasks".
Users can create "Active Modules" which allow Athena to respond to different commands.
The "Weather" module, for example, handles questions like "Is it cold outside?", "What is the forecast for tonight?"

Active Tasks
------------
An Active Task looks for matches in user input to decide whether or not to execute an action.
If the task's "match" method returns true, then the task action is added to the module's task queue.

Input Matching Order
--------------------
Both Active Modules and Active Tasks have a "priority" attribute and a "greedy" attribute.

For priority, higher number means the module or task is matched/executed first (e.g. - priority 5 is executed before priority 1)

If a module or task is greedy, then no other lower priority modules or tasks can match/execute afterward.

**Here is a basic idea of the input matching scheme:**

.. code:: python

    sort modules based on priority 
    for each mod in modules:
        mod.task_queue = []
        for each task in sorted(mod.tasks):
            if task.match(text):
                mod.task_queue.append(task)
                if task.greedy:
                    break

            if mod matched one or more tasks:
                self.matched_mods.append(mod)

Roadmap
-------
Hey Athena is just getting started. We plan to build an open-source community built around our voice assistance framework. Here are some features you can expect to see in the future:

- **Passive Modules:** useful for voice/text notifications (e.g. - Unread email, Twitter notifications)
- **Web App Demo:** we are in the process of making a simple web app demo for Hey Athena
- **Bigger Community:** we are working on building a bigger open-source community
- **HTTP REST API Service:** users will be able to send HTTP requests and receive a voice/text JSON response (e.g. - ``HTTP GET http://heyathena.com/api/{api_key}/q=list%20bitcoin%20price``) 

.. |Graphic Overview| image:: https://heyathena.com/img/graphic.png
   :target: https://heyathena.com/img/graphic.png