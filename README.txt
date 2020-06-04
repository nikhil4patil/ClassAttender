Written By: Nikhil Patil :)

Hey there! The purpose of this script is to make sure that you never miss a meeting!
And at the same time, you never have to even worry about missing a meeting, as long
as you are not asleep and actively working.

MeetingAttender simply allows you to do whatever work you are doing until the last minute,
when it steps in and launches your meeting for you. Although it seems rather trivial, it does
improve efficiency and reduces the number of things you need to keep track of.

How does it work?
	Once the user enters when their meeting is and provides a link for it. The script
	detects which OS it's being executed on, and based on that makes some changes.
	If it's a Windows OS, then it creates Tasks in the Task Scheduler to run the batch
	script to execute the program before the next meeting time.
	For other OS, it runs in the background and puts itself to sleep until the next
	meeting time.

This file contains the info on how to make the ClassAttender.py run from
scratch. A) Install Python and Anaconda B) Update the Python and Browser
paths in ClassAttender.py C) Install Python libraries needed for the
ClassAttender.py to function D) Update the openClass function in
ClassAttender.py based on your needs.

A)  Install Anaconda
    1) Go to https://www.anaconda.com/distribution/\#download-section
       and install the Python 3.7+ version

B)  Update Python path
    1) Open the command prompt or cmd 1.1) Press Windows or Start key
       on your keyboard 1.2) Type in cmd and hit enter. This should
       open a command prompt (aka cmd)
    2) Enter "where python" in the cmd and hit enter
    3) In the output, there should be one or multiple lines showing you
       where python.exe file is stored
    4) Find the line that has Anaconda in it and copy that entire line
       (the absolute path)
    5) Open ClassAttender.py file and replace the python\_path variable (around line 30)
		5.1) The line should be updated to:
        python\_path = r'<the absolute path you found>'

B2) Update Chrome path 
	1) Find the exe for whichever browser you prefer to use 
	2) For Chrome the path should stay the same but feel free to double check 
	   2.1) Chrome: r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
	   2.2) IE: 	r'C:/Program Files/Internet Explorer/iexplore.exe'

C)  Install Python Libraries
    1) Open terminal/cmd (step 1 of part A shown above)
    2) Enter the following commands and hit enter. Wait for cmd to
       finish executing before moving onto the next one 2.1) pip
       install opencv-python 2.2) pip install pyautogui

D)  Change openClass as you see fit. The general flow is:
    1) Launch a web page
    2) Sleep for it to load
    3) Tell findAndClick("image\_or\_button\_to\_find") to find and
       click something

Sources used: 
Template Matching:
	https://opencv-python-tutroals.readthedocs.io/en/latest/py\_tutorials/py\_imgproc/py\_template\_matching/py\_template\_matching.html
Task Scheduler from CMD:
	https://www.windowscentral.com/how-create-task-using-task-scheduler-command-prompt
	https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks
