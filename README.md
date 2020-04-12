Brilliant but borderline lazy genius who wrote this: Nikhil Patil :)

This script will only create Tasks in the Task Scheduler if it's running on a Windows machine.
For any other OS, the script will be executed continuously in the background.

This file contains the info on how to make the ClassAttender.py run from scratch.
A) Install Python and Anaconda
B) Update the Python and Browser paths in ClassAttender.py
C) Install Python libraries needed for the ClassAttender.py to function
D) Update the openClass function in ClassAttender.py based on your needs.



A) Install Anaconda
    1) Go to https://www.anaconda.com/distribution/#download-section and install the Python 3.7+ version

B) Update Python path
    1) Open the command prompt or cmd
        1.1) Press Windows or Start key on your keyboard
        1.2) Type in cmd and hit enter. This should open a command prompt (aka cmd)
    2) Enter "where python" in the cmd and hit enter
    3) In the output, there should be one or multiple lines showing you where python.exe file is stored
    4) Find the line that has Anaconda in it and copy that entire line (the absolute path)
    5) Open ClassAttender.py file and replace the python_path variable (around line 30)
        5.1) The line should be updated to: python_path = r'<the absolute path you found>'

B.2) Update Chrome path
    1) Find the exe for whichever browser you prefer to use
    2) For Chrome the path should stay the same but feel free to double check
        2.1) Chrome: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        2.2) IE: r'C:\Program Files\Internet Explorer\iexplore.exe'

C) Install Python Libraries
    1) Open terminal/cmd (step 1 of part A shown above)
    2) Enter the following commands and hit enter. Wait for cmd to finish executing before moving onto the next one
        2.1) pip install opencv-python
        2.2) pip install pyautogui

D) Change openClass as you see fit. The general flow is:
    1) Launch a web page
    2) Sleep for it to load
    3) Tell findAndClick("image_or_button_to_find") to find and click something


Sources used:
    Template Matching:
        https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    Task Scheduler from CMD:
        https://www.windowscentral.com/how-create-task-using-task-scheduler-command-prompt
        https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks
