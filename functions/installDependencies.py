## Dependency installation system by AgentLoneStar007
## https://github.com/AgentLoneStar007

import json
import subprocess
from functions.logger import Log
from functions.loadData import loadAppData
from data.colors import Colors
import tkinter as tk
import tkinter.font as tkFont
from tkinter import Scrollbar


def loadDependencies():
    # Open dependencies file and load data into memory
    with open('data/dependencies.json', 'r') as file:
        depends = json.load(file)
        file.close()

    # Create lists for dependency names, import code, and install commands
    dependNames = []
    dependImport = []
    dependInstall = []
    dependRequired = []

    # Import the data into the lists
    for x in depends["dependencies"]:
        dependNames.append(x['name'])
        dependImport.append(x['import'])
        dependInstall.append(x['install'])
        dependRequired.append(x['required'])

    # When the function is used, return the lists
    return dependNames, dependImport, dependInstall, dependRequired


def graphicalInstall(logFile: str, failedInstalls: list):
    def gInstall2():
        def gInstall3():
            def gInstall4():
                print(window)
                # Destroy the window and specify that it is no longer active
                window.destroy()
                global isWindowAlive
                isWindowAlive = False
                # Continue with program
                return

            # Define if window is alive - there's probably a better way to do this
            global isWindowAlive # If I don't define it globally both times, it causes an error
            isWindowAlive = True

            # If any dependencies failed, update the top label to give more information, and update the button to quit
            # the program
            if len(failedInstalls) >= 1:
                for x in failedInstalls:
                    if required[(names.index(x))]:
                        header['text'] = 'Required dependencies failed to install.\nCannot continue.'
                        mainButton2.destroy()
                        mainButton3 = tk.Button(window)
                        mainButton3["text"] = "Quit"
                        mainButton3["command"] = lambda: quit()
                        mainButton3.place(x=325, y=270, width=70, height=25)
                        window.update()
                        # Must start a main loop; otherwise window will close immediately
                        window.mainloop()

                header['text'] = 'Some dependencies failed to install, but they \nare optional. Do you want to continue?'
                mainButton2["text"] = "Quit"
                mainButton2["command"] = lambda: quit()
                mainButton2.place(x=250, y=270, width=70, height=25)
                mainButton3 = tk.Button(window)
                mainButton3["text"] = "Continue"
                mainButton3["command"] = lambda: gInstall4()
                mainButton3.place(x=325, y=270, width=70, height=25)
                window.update()
                # Must start a main loop; otherwise window will close immediately
                window.mainloop()

            # Quit the window and continue with the program otherwise
            if isWindowAlive:
                window.destroy()

        # Update the window for autoinstall
        ## Update content box
        header['text'] = 'Attempting installation...'
        contentBox['bg'] = '#000000'
        contentBox.delete('1.0', 'end')
        contentBox['font'] = tkFont.Font(family='Fixedsys', size=8)
        ## Destroy unneeded items
        footerLabel.destroy()
        mainButton.destroy()  # pack_forget() isn't working, so we use destroy()
        quitButton.destroy()
        window.update()

        # Install the dependencies
        anyFailed = False

        # Function to search the content box and find the last printed message, then tag it
        def search(keyword, tag):
            pos = '1.0'
            while True:
                idx = contentBox.search(keyword, pos, 'end')
                if not idx:
                    break
                pos = '{}+{}c'.format(idx, len(keyword))
                contentBox.tag_add(f'{tag}', idx, pos)

        # I used Y here because X was used earlier
        for y in failedInstalls:
            # Attempt to install the dependency
            process = subprocess.Popen(installs[names.index(y)], shell=True, stdout=subprocess.PIPE)
            process.wait()
            # If successful, continue
            if process.returncode == 0:
                # Create the message, insert it into the content box...
                message = f'Installed dependency {y} successfully. Continuing...'
                contentBox.insert('insert', message + '\n\n')
                # Then use search() to tag it, and use the tag to color it accordingly
                search(message, y)
                contentBox.tag_config(f'{y}', foreground="green")
                # Finally log it all
                Log(logFile, 'info', f'Installed dependency {y} successfully.')

            # If unsuccessful, give name and install command of the module, then continue
            else:
                # If any dependency failed to install, update the anyFailed var to true
                anyFailed = True
                # See above for explanation of the following
                message = f'Install of {y} failed. If you wish to attempt a manual installation, the install command ' \
                          f'should be "{installs[names.index(y)]}".'
                contentBox.insert('insert', message + '\n\n')
                search(message, y)
                contentBox.tag_config(f'{y}', foreground="red")
                Log(logFile, 'err',
                             f'Failed to autoinstall dependency {y}. Command exited with code "{process.returncode}."')
            # Every time the for loops goes through and attempts a dependency installation, update the window
            window.update()

        # Once installation is complete, create a new button to continue to the next part
        mainButton2 = tk.Button(window)
        mainButton2["text"] = "Continue"
        mainButton2["command"] = lambda: gInstall3()
        mainButton2.place(x=325, y=270, width=70, height=25)
        window.update()

    # Load the data - there's probably a more efficient way of doing this
    names, imports, installs, required = loadDependencies()

    # Create the window and set some specs
    window = tk.Tk()
    window.geometry('400x300')
    window.resizable(width=False, height=False)
    window.title(loadAppData()['name'] + ' - Dependencies')

    # Create the individual elements
    ## Header
    header = tk.Label(window)
    header['font'] = tkFont.Font(size=13)
    header['justify'] = 'center'
    header['text'] = 'Failed to load the following dependencies:'
    header.place(x=-1, y=0, width=400, height=64)

    ## Content box (first lists dependencies, then output of installation after window update)
    contentBox = tk.Text(window, wrap='word')
    contentBox['borderwidth'] = '3px'
    contentBox['font'] = tkFont.Font(family='Times', size=12)
    contentBox['bg'] = '#B2B2B2'
    # Add every failed dependency to the listbox
    for x in failedInstalls:
        contentBox.insert('end', x + '\n')
    contentBox.place(x=10, y=80, width=382, height=144)

    ## Scrollbar - In case there's a lot of output
    scrollbar = Scrollbar(contentBox, orient='vertical', width=7)
    scrollbar.pack(side='right', fill='both')
    contentBox.config(yscrollcommand=scrollbar.set)

    ## Footer label
    footerLabel = tk.Label(window)
    footerLabel["font"] = tkFont.Font(size=10)
    footerLabel["justify"] = "center"
    footerLabel["text"] = "Would you like to attempt to autoinstall these dependencies?"
    footerLabel.place(x=0, y=230, width=400, height=30)

    ## Approve autoinstall button - continues to next part
    mainButton = tk.Button(window)
    mainButton["justify"] = "center"
    mainButton["text"] = "Yes"
    mainButton["command"] = lambda: gInstall2()
    mainButton.place(x=325, y=270, width=70, height=25)

    ## Deny autoinstall button - exits program
    quitButton = tk.Button(window)
    quitButton["justify"] = "center"
    quitButton["text"] = "Quit"
    quitButton["command"] = lambda: quit()
    quitButton.place(x=250, y=270, width=70, height=25)

    # Run the window and log it
    Log(logFile, 'debug', 'Created dependency installation window.')
    window.mainloop()


def terminalInstall(logFile: str, failedImports: list):
    # Load the data
    names, imports, installs, required = loadDependencies()

    # Print dependencies needing installation
    print(f'{Colors.ForeG.yellow}Could not load dependency(s) ', end='')
    # Do some formatting so the list looks good
    for x in failedImports:
        # If there's only one item in the list, print it like, "(item)."
        if len(failedImports) == 1:
            print(f'{x}.', end='')
            break
        # If the current item is last in the list, print it like, "and (item)."
        if x == failedImports[-1]:
            print(f'and {x}.', end='')
            break
        print(f'{x}, ', end='')
    print(f'{Colors.reset}')

    # Log the failed dependencies
    Log(logFile, 'err', f'Could not load dependency(s): {failedImports}.')

    # Attempt autoinstall
    autoInstall = input(f'Would you like to attempt an autoinstall? <Y/n> ')
    if autoInstall.lower() == 'y' or autoInstall == '':
        failedInstalls = []
        for x in failedImports:
            # Run the given installation command and log it as debug
            Log(logFile, 'debug', f'Attempting autoinstall of {x} with command'
                                  f"{installs[names.index(x)]}.")
            process = subprocess.Popen(installs[names.index(x)], shell=True, stdout=subprocess.PIPE)
            process.wait()
            # If successful, continue
            if process.returncode == 0:
                print(f'{Colors.ForeG.green}Installed dependency {x} successfully. '
                      f'Continuing...{Colors.reset}')
                Log(logFile, 'info', f'Installed dependency {x} successfully.')

            # If unsuccessful, give name and install command of the module, then continue
            else:
                failedInstalls.append(x)
                print(f'{Colors.ForeG.red}Install failed. If you wish to attempt a manual installation, '
                      f'the name of the module is {x}, and the install command should be '
                      f'"{installs[names.index(x)]}".{Colors.reset}')
                Log(logFile, 'err', f'Failed to autoinstall dependency {x}. Command '
                             f'exited with code "{process.returncode}."')

        # If any dependencies failed to install, check if they were required
        if len(failedInstalls) >= 1:
            for x in failedInstalls:
                if required[(names.index(x))]:
                    print(f'{Colors.ForeG.red}Required dependency {x} failed to install. Cannot continue.')
                    input(f'Press Enter to exit...{Colors.reset}')
                    quit()
            print(f'{Colors.ForeG.yellow}Some dependencies failed to install, but they are optional.')
            ans = input('Do you want to continue? <Y/n> ')
            if ans.lower() == 'y' or ans == '':
                return
            else:
                quit()

    # If user does not attempt autoinstall, exit the program
    else:
        print(f'{Colors.ForeG.red}Program cannot continue without these dependencies.')
        input(f'Press Enter to exit...{Colors.reset}')
        quit()


class InstallDependencies:
    def __init__(self, logFile):
        # Check to see if app type is terminal or graphical
        appType = loadAppData()['app-type']

        # Get dependencies that need installation, if any
        names, imports, installs, required = loadDependencies()

        # If the lists aren't empty, run the following code - change this if you have no dependencies needing
        # installation.
        if names is not None and imports is not None and installs is not None:
            failedImports = []

            # For each item in the lists, attempt to import it
            for x in imports:
                try:
                    exec(x)

                # If failed, add the item to a list of dependencies that need installation
                except:
                    failedImports.append(names[imports.index(x)])

            # If there are any failed imports, run the error dialogue/autoinstaller
            if len(failedImports) >= 1:
                # If graphical, use graphical installation. If terminal, use terminal installation.
                if appType == 'graphical':
                    graphicalInstall(logFile, failedImports)
                else:
                    terminalInstall(logFile, failedImports)

        # If any of the three lists are empty, exit. Modify this code  to not exit if you don't need any dependencies to
        # be installed for some reason.
        else:
            print(f'{Colors.ForeG.red}Dependency file is empty, for some reason. Unable to continue.')
            input(f'Press Enter to exit...{Colors.reset}')
            quit()
