## Dependency installation system by AgentLoneStar007
## https://github.com/AgentLoneStar007

import json
import subprocess
from functions.logger import Log
from data.colors import Colors
from functions.loadData import loadAppData


def loadData():
    # Open dependencies file and load data into memory
    with open('data/dependencies.json', 'r') as file:
        depends = json.load(file)
        file.close()

    # Create lists for dependency names, import code, and install commands
    dependNames = []
    dependImport = []
    dependInstall = []

    # Import the data into the lists
    for x in depends["dependencies"]:
        dependNames.append(x['name'])
        dependImport.append(x['import'])
        dependInstall.append(x['install'])

    # When the function is used, return the lists
    return dependNames, dependImport, dependInstall


def graphicalInstalls(logFile: str, failedInstalls: list):
    return


def terminalInstalls(logFile: str, failedInstalls: list):
    # Load the data - there's probably a more efficient way of doing this
    names, imports, installs = loadData()

    # Print dependencies needing installation
    print(f'{Colors.ForeG.yellow}Could not load dependency(s) ', end='')
    # Do some formatting so the list looks good
    for x in failedInstalls:
        # If there's only one item in the list, print it like, "(item)."
        if len(failedInstalls) == 1:
            print(f'{x}.', end='')
            break
        # If the current item is last in the list, print it like, "and (item)."
        if x == failedInstalls[-1]:
            print(f'and {x}.', end='')
            break
        print(f'{x}, ', end='')
    print(f'{Colors.reset}')

    # Log the failed dependencies
    Log(logFile, 'err', f'Could not load dependency(s): {failedInstalls}.')

    # Attempt autoinstall
    autoInstall = input(f'Would you like to attempt an autoinstall? <Y/n> ')
    if autoInstall.lower() == 'y':
        anyFailed = False
        for x in failedInstalls:
            # Run the given installation command and log it as debug
            Log(logFile, 'debug', f'Attempting autoinstall of {x} with command'
                                  f"{installs[names.index(x)]}.")
            process = subprocess.Popen(installs[names.index(x)], shell=True, stdout=subprocess.PIPE)
            process.wait()
            # If successful, close the program.
            if process.returncode == 0:
                print(f'{Colors.ForeG.green}Installed dependency {x} successfully. '
                      f'Continuing...{Colors.reset}')
                Log(logFile, 'info', f'Installed dependency {x} successfully.')

            # If unsuccessful, give name and install command of the module, then continue
            else:
                anyFailed = True
                print(f'{Colors.ForeG.red}Install failed. If you wish to attempt a manual installation, '
                      f'the name of the module is {x}, and the install command should be'
                      f'"{installs[names.index(x)]}".{Colors.reset}')
                Log(logFile, 'err', f'Failed to autoinstall dependency {x}. Command '
                             f'exited with code "{process.returncode}."')

        # If any dependencies failed to install, exit the program
        if anyFailed:
            print(f'{Colors.ForeG.red}Some dependencies failed to install. Cannot continue.')
            input(f'Press Enter to exit...{Colors.reset}')
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
        names, imports, installs = loadData()

        # If the lists aren't empty, run the following code - change this if you have no dependencies needing
        # installation.
        if names is not None and imports is not None and installs is not None:
            failedInstalls = []

            # For each item in the lists, attempt to import it
            for x in imports:
                try:
                    exec(x)

                # If failed, add the item to a list of dependencies that need installation
                except:
                    failedInstalls.append(names[imports.index(x)])

            # If there are any failed imports, run the error dialogue/autoinstaller
            if len(failedInstalls) >= 1:
                # If graphical, use graphical installation. If terminal, use terminal installation.
                if appType == 'graphical':
                    graphicalInstalls(logFile, failedInstalls)
                else:
                    terminalInstalls(logFile, failedInstalls)

        # If any of the three lists are empty, exit. Modify this code  to not exit if you don't need any dependencies to
        # be installed for some reason.
        else:
            print(f'{Colors.ForeG.red}Dependency file is empty, for some reason. Unable to continue.')
            input(f'Press Enter to exit...{Colors.reset}')
            quit()
