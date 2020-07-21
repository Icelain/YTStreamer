import subprocess
import pyautogui
import pyperclip

def cls():
    subprocess.call("clear")

def listToString(lst):
    return "".join(lst)

def _workaround_write(text):
    """
    This is a work-around for the bug in pyautogui.write() with non-QWERTY keyboards
    It copies the text to clipboard and pastes it, instead of typing it.
    """
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy('')
