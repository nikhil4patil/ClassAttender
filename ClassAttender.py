"""
    Author: Nikhil Patil
    Project: ClassAttender
    Purpose:
        We love efficiency. Being a software engineer and someone who likes to have fun, I created this project
    to allow me to sleep in or play games until the last minute possible. And also to ensure that I don't forget to
    attend my class sessions.

    Code:
        1) Read the classes.txt file to find the time and day of my classes. Along with the link and any other details.
        2) Create a batch file that will be executed by the Task Scheduler to run this script
        3) Create tasks in the Task Scheduler that runs the batch script whenever one of your sessions is about to begin
        4) When executed, this script will check if any of your classes are about to begin in 3 minutes or began 3
           minutes ago. If so, the script will launch the site and join the live session for you.
"""

import os
import subprocess
from datetime import datetime
import cv2
import pyautogui
import webbrowser
from time import sleep
import platform


# Get the current time
currTime = datetime.now()
# Find today: MON, TUE, WED, THU, FRI, SAT, SUN
today = currTime.strftime("%a").upper()
# Define the path to chrome exe
browser_path = r'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# Path to python
python_path = r'C:\ProgramData\Anaconda3\python.exe'


# Launches the session
def openClass(info):
    # For elearning collaborate session
    if 'elearning' in info[0]:
        # Open the elearning page
        webbrowser.get(browser_path).open('https://elearning.utdallas.edu')

        sleep(3) # Wait for page to load. Sleep for 3 seconds
        # Click Login if on the login screen
        findAndClick('elearningLogin.png')

        sleep(2)  # Wait for authentication
        # Launch the session link
        webbrowser.get(browser_path).open(info[0])

        # For the professors that created Regular class sessions
        if 'Regular' in info:
            sleep(5)
            # Find and click on the regular class icon
            findAndClick('regularClass.png')
        else:
            sleep(5)
            # Find the course room button
            findAndClick('courseRoom.png')
            sleep(1)
            # Find the join room button
            findAndClick('joinCourseRoom.png')
    # For webex meetings
    elif 'webex' in info[0]:
        # Go to the link
        webbrowser.get(browser_path).open(info[0])
        sleep(10) # Wait for WebEx web client to load
        # Find the join meeting button and start session
        findAndClick('webexJoinMeeting.png')


# Takes a screenshot of the screen, find the specified sub-image in the screenshot, click it
def findAndClick(findSS=""):
    screen = pyautogui.screenshot()
    # Save the screenshot as screenshot.png
    screen.save(r'screenshot.png')
    # Creates a grayscale image
    img = cv2.imread('screenshot.png', 0)
    template = cv2.imread(findSS, 0)

    # Finds the width and height of the template/button
    w, h = template.shape[::-1]

    # Specify the template being used
    method = cv2.TM_SQDIFF_NORMED

    # Apply template Matching
    res = cv2.matchTemplate(img, template, method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Used as a threshold measure. Smaller the number the better match it is
    if min_val > 0.01:
        return

    # Find the top left of the image
    top_left = min_loc
    # Find the center of the button
    button_center = (int(top_left[0] + w / 2), int(top_left[1] + h / 2))

    # print(button_center) # Prints the (x, y) coordinate of the center

    # Cute little animation of moving the mouse to the button
    pyautogui.moveTo(*button_center, duration=0.5)
    # Press the button
    pyautogui.click(*button_center)


# Get the class schedule
def getClasses(filePath="classes.txt"):
    data = []
    with open(filePath, "r") as file:
        for line in file.readlines():
            line.replace('\n', '')
            info = line.split(", ")

            # Allow some comments in the classes.txt file
            if '#' in info[0] or '//' in info[0] or len(info) < 4:
                continue

            # Get the class name. Used while creating task later
            className = info[0]
            # Store the time on 24 hr clock
            classTime = datetime.strptime(info[1], '%I:%M %p')

            # Create a list of 3-letter day names, in uppercase
            classDays = info[2].split()
            temp = []
            for day in classDays:
                temp.append(day.upper())
            classDays = temp

            # Append info to data
            data.append([className, classTime, classDays, info[3:]])
    return data


# Create tasks in the Task Scheduler
def createTasks(data, batPath="{}\\classAttender.bat".format(os.getcwd())):
    if batPath is None or len(data) == 0:
        return

    for item in data:
        # Get the days from the list without the [] or ''
        days = ""
        for day in item[2]:
            days += "{},".format(day)
        days = days[:-1]

        # Query to create a Task in Task Scheduler with the name of the class for each class
        # Repeats every week on specified date and time
        cmd = r"schtasks /create /tn {}ClassAttender /tr {} /sc weekly /d {} /st {:02d}:{:02d} /f"\
            .format(item[0], batPath, days, item[1].hour, item[1].minute)

        # Execute the command to create the task
        os.system(cmd)


# Create a batch file that will be executed by the task scheduler
def createBatch(batName="classAttender.bat"):
    # Changes directory to current directory
    # Executes the python script using python path provided above
    # Exit the batch script
    with open(batName, 'w') as file:
        file.writelines([r'cd {}'.format(os.getcwd()), '\n',
                         r'{} {}'.format(python_path, __file__), '\n',
                         r'exit'])
    # Return the absolute path to the batch file
    return "{}\\{}".format(os.getcwd(), batName)


# Deletes any previously scheduled tasks
def deleteTasks():
    # Find all tasks with ClassAttender in their names
    for line in subprocess.Popen("schtasks | findstr ClassAttender",
                                 shell=True, stdout=subprocess.PIPE).stdout.readlines():
        line = line.decode("utf-8")
        # Extract the class name
        className = line.split('ClassAttender')[0]
        if len(className) > 0:
            # Remove the task
            cmd = r"schtasks /delete /tn {}ClassAttender /f".format(className)
            os.system(cmd)


def main():
    data = getClasses()

    # Check if the batch file exists or not
    if 'Windows' in platform.system() and os.path.exists("classAttender.bat") is False:
        # Create the batch file
        batPath = createBatch()
        # Delete previous tasks
        deleteTasks()
        # Create tasks that start this script whenever a session is about to start
        createTasks(data, batPath)

    for item in data:
        classTime = item[1]

        # Find the difference between current time and when the session begins
        hourDiff = (classTime.time().hour - currTime.time().hour)
        minDiff = (classTime.time().minute - currTime.time().minute)
        timeDiff = abs(hourDiff * 60 + minDiff)
        # print(classTime.time(), currTime.time(), timeDiff)

        # If the session begins in or began 5 minutes ago, launch the session
        if timeDiff < 5 and today in item[2]:
            openClass(item[3:])


if __name__ == "__main__":
    main()
