# Brian Oliver 001321694

import msvcrt as m
from wgups.objects.clock import Clock
from wgups.objects.package import Package
from wgups.ui.cli import GUI
from wgups.controller.delivery_controller import DeliveryController
import time

# Credit to Stackoverflow for the following code to maximize consoles--
# https://stackoverflow.com/questions/43959168/python-console-fullscreen-maybe-using-os-system
import os
import ctypes
import subprocess

from ctypes import wintypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)


def maximize_console(lines=None):
    """
    This function maximizes the console/terminal running the script.

    Notes from StackOverflow: It uses ctypes to call WinAPI functions.
    First it calls GetLargestConsoleWindowSize in order to figure how
    big it can make the window, with the option to specify a number of
    lines that exceeds this in order to get a scrollback buffer. To do
    the work of resizing the screen buffer it simply calls mode.com
    via subprocess.check_call. Finally, it gets the console window
    handle via GetConsoleWindow and calls ShowWindow to maximize it.

    :param lines: Needed if you would like to create a scrollback buffer
    to exceed the number of lines that can be shown in a window.
    :return: None

    Space Complexity
        O(n)

    Time Complexity
        O(1)
    """
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = m.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
            cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

# END CREDIT
# ---------------------------------------------------------------------

def escape_listener(cli):
    """
    Checks if the ESC key was pressed. If so, it will display the
    prompt asking the user if they would like to quit the program.
    If the user enters Y, the program with exit
    :param cli: The GUI object that should show the exit prompt.

    Space-Complexity
        O(1)

    Time-Complexity
        O(1)

    """
    if m.kbhit():
        key = ord(readch())
        if key == 27:
            if system_exit_prompt():
                cli.exit()


def system_exit_prompt() -> bool:
    """
    Prints a prompt asking the user if they would like to exit the
    program. If the user enters Y or y, the program will true. Any
    other input will return false.
    :return: True if the user's input is Y or y. Otherwise, false.

    Space-Complexity
        O(1)

    Time-Complexity
        O(1)
    """
    answer = input("\u001b[31mAre you sure you want to exit the program? \u001b[0m(Y/n): ")
    if str.upper(answer) == "Y":
        return True
    else:
        return False


def readch():
    """
    Get a single character on Windows.

    see https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/getch-getwch?view=vs-2019

    This function is needed to provide the escape key quit function.

    *** Credit to StackOverflow question and answer found on
    https://stackoverflow.com/questions/21653072/exiting-a-loop-by-pressing-a-escape-key

    Space Complexity
        O(n)
    Time Complexity
        O(n)
    """
    ch = m.getch()
    if ch in b'\x00\xe0':  # Checks to see if there is an arrow or function key prefix.
        ch = m.getch()
    return ch


def get_any_key_prompt():
    """
    This function pauses the program until any key input is received.

    Space-Complexity
        O(1)

    Time-Complexity
        O(1)
    """
    print("\n\nPress any key to continue...", end="\r")
    m.getch()
    print("Loading information hud....")


def main_loop(cli, data_controller, fast_mode=False):
    """
    The main loop that controls the flow of the program. The main loop
    consists of the following flow:
        1. Check for a KeyboardInterrupt (ctrl+C) or ESC key press. If
        the key is found. Display the appropriate exit/search prompts.
        If not, go to step 2.

        2. Call the GUI (wgups.ui.cli) tick method to update the GUI with
        any updated information since the last tick call.

        3. Call the DeliveryController (wgups.controller.delivery_controller)
        tick method to cause data logic functions to fire.

    :param cli: The GUI object created in the main function
    :param data_controller: The DeliveryController object created in the main function
    :param fast_mode: True if you would like the program to avoid built
    in delays.

    Space-Complexity
        O(n)

    Time-Complexity
        O(n)
    """

    # Try statement is placed before the loop to allow the loop to be
    # interrupted when ctrl+c is pressed.
    try:
        while True:
            # Check to see if escape is pressed.
            escape_listener(cli)

            # If escape is pressed, this will not fire until the
            # program is resumed. The GUI is updated first with the
            # most recent information, then the delivery_controller is
            # allowed to make any changes to the data before the next
            # tick. This kind of gives the appearance of threads
            # without having to actually use threads.
            cli.tick()
            data_controller.tick()

            # If fast mode is false, the program will sleep for 1
            # second. This gives the illusion of seeing the program
            # update in real time to show the package deliveries.
            if fast_mode is False:
                time.sleep(1)

    # If ctrl+C was pressed, display package search prompt
    except KeyboardInterrupt:
        while True:
            package_id = input("\u001b[31m(Type r to resume)\u001b[0m Enter the Package #: ")

            # if user input's r, then the main loop will resume.
            if str.lower(package_id) == "r":
                break

            # Search package number if it is a number 1-40. Otherwise,
            # the user will be prompted to enter the package number
            # again.
            try:
                if 0 < int(package_id) < 41:
                    cli.show_package(Package.master_package_list[int(package_id) - 1])
                    get_any_key_prompt()
                    break
                else:
                    print("Enter a package number between 1-40 or q to exit.")
            except ValueError:
                print("Enter a package number between 1-40 or q to exit.")

        # Restart the main loop
        main_loop(cli, data_controller)


if __name__ == '__main__':
    """
    Creates the clock, DeliveryController, and GUI objects that the 
    program will use. The console that ran the script is maximized and
    the main loop is started.
    
    Space-Complexity = O(1)
    Time-Complexity = O(n)
    """
    app_clock: Clock = Clock()
    # Initialize GUI and data controller objects
    cli = GUI(clock=app_clock)
    data_controller = DeliveryController(clock=app_clock)

    # Load objects before starting cli gui and running data logic loop
    data_controller.start()

    # Maximizes the console. This is needed since the data is
    # represented in a way that utilizes a large amount of screen
    # space
    maximize_console()

    # Starts the main loop and keeps the program persisting.
    while True:
        main_loop(cli, data_controller)
