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
        O(N)

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


# ---------------------------------------------------------------------

def escape_listener(cli):
    if m.kbhit():
        key = ord(readch())
        if key == 27:
            if system_exit_prompt():
                cli.exit()


def system_exit_prompt() -> bool:
    answer = input("\u001b[31mAre you sure you want to exit the program? \u001b[0m(Y/n): ")
    if answer == "Y":
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
    """
    ch = m.getch()
    if ch in b'\x00\xe0':  # Checks to see if there is an arrow or function key prefix.
        ch = m.getch()
    return ch


def get_any_key_prompt():
    print("\n\nPress any key to continue...", end="\r")
    m.getch()
    print("Loading information hud....")


def main_loop(cli, data_controller, fast_mode=False):
    try:
        while True:
            escape_listener(cli)
            cli.tick()
            data_controller.tick()
            if fast_mode is False:
                time.sleep(1)

    except KeyboardInterrupt:
        while True:
            package_id = input("\u001b[31m(Type r to resume)\u001b[0m Enter the Package #: ")
            if str.lower(package_id) == "r":
                break
            try:
                if 0 < int(package_id) < 41:
                    cli.show_package(Package.package_list[int(package_id) - 1])
                    get_any_key_prompt()
                    break
                else:
                    print("Enter a package number between 1-40 or q to exit.")
            except ValueError:
                print("Enter a package number between 1-40 or q to exit.")

        main_loop(cli, data_controller)


if __name__ == '__main__':
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

    while True:
        main_loop(cli, data_controller)
