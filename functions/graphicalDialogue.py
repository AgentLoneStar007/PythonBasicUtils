from functions.logger import Log
from functions.loadData import loadAppData
import tkinter as tk
import textwrap


class GDialogue:
    # The arguments are as follows: message to show, message to log(if different from message to show; if not, pass None
    # as the arg), and custom buttons. Pass a dictionary in for custom buttons with a format of {"buttonName":"command"}
    def __init__(self, message: str, messageToLog, windowTitle, custom_buttons, logFile: str):
        # Load the app's name
        appName = loadAppData()['name']

        # If the messageToLog is a string, go ahead and log it
        if type(messageToLog) == str:
            Log(logFile, 'err', messageToLog)
        else:
            Log(logFile, 'err', message)

        # If message is too long, make it run over multiple lines
        if len(message) > 40:
            message = textwrap.fill(message, 40)
        # If message is longer than 10-ish lines, make it stop at 10 lines
        if message.count('\n') > 10:
            i = message.index('\n', 340)
            # A little formatting to make the dots appended look nice
            if message[i] == '.':
                message = message[:i] + '..'
            else:
                message = message[:i] + '...'

        # If the window title arg is a string and not too long, set the window's title to equal it
        # Otherwise, set it as "Error."
        if type(windowTitle) == str and len(windowTitle) <= 20:
            title = windowTitle
        else:
            title = f'{appName} - Error'

        # Create the window
        window = tk.Tk()
        # Set the window title and make it non-resizable
        window.title(title)
        window.resizable(False, False)
        # Insert the message provided into the window
        label = tk.Label(window, text=message)
        label.pack(fill='x', padx=70, pady=20)

        # Create a close button
        button_close = tk.Button(window, text="OK", width=7, command=window.destroy)
        button_close.pack(anchor='e', padx=5, pady=5, side=tk.RIGHT)

        # Create, if any, custom buttons.
        if type(custom_buttons) == dict:
            for x in custom_buttons:
                buttonLength = len(x)
                y = tk.Button(window, text=x, width=buttonLength, command=lambda: exec(custom_buttons[x]))
                y.pack(anchor='e', padx=5, pady=5, side=tk.RIGHT)

        # Keep the window running until closed
        window.mainloop()

