import os
import subprocess
from datetime import datetime
import cv2
import pyautogui
import webbrowser
from time import sleep

# Get the current time
currTime = datetime.now()
# Find today: MON, TUE, WED, THU, FRI, SAT, SUN
today = currTime.strftime("%a").upper()
# Define the path to chrome exe
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# Path to python
python_path = r'C:\ProgramData\Anaconda3\python.exe'


# Takes a screenshot of the screen, and finds the specified sub-image after sleeping for a bit
def findAndClick(findSS="", zzz=3):
    sleep(zzz)
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


# Launches the session
def openClass(info):
    # For elearning collaborate session
    if 'elearning' in info[0]:
        # Open the elearning page
        webbrowser.get(chrome_path).open('https://elearning.utdallas.edu')
        # Click Login if on the login screen
        findAndClick('elearningLogin.png', 3)
        sleep(2)  # Wait for authentication
        # Launch the session link
        webbrowser.get(chrome_path).open(info[0])

        # For the professors that created Regular class sessions
        if 'Regular' in info:
            # Find and click on the regular class icon
            findAndClick('regularClass.png', 5)
        else:
            # Find the course room button
            findAndClick('courseRoom.png', 5)
            # Find the join room button
            findAndClick('joinCourseRoom.png', 1)
    # For webex meetings
    elif 'webex' in info[0]:
        # Go to the link
        webbrowser.get(chrome_path).open(info[0])
        # Find the join meeting button and start session
        findAndClick('webexJoinMeeting.png', 10)


# Get the class schedule
def getClasses(filePath="classes.txt"):
    data = []
    with open(filePath, "r") as file:
        for line in file.readlines():
            line.replace('\n', '')
            info = line.split(", ")

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
    if os.path.exists("classAttender.bat") is False:
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
