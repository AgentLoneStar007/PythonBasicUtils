## Dependency installation system by AgentLoneStar007
## https://github.com/AgentLoneStar007

import json
import subprocess
from functions.logger import Log
from data.colors import Colors


def loadData():
    # Open dependencies file and load data into memory
    with open('data/dependencies.json', "r") as file:
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


class InstallDependencies:
    def __init__(self, logFile):
        print('Testing for dependencies...')
        names, imports, installs = loadData()

        # If the lists aren't null, run the following code
        if names is not None and imports is not None and installs is not None:
            # For each item in the lists
            for x in imports:
                currentItem = imports.index(x)

                # Try to import the item
                try:
                    exec(x)

                # If failed, attempt autoinstall
                except:
                    print(f'{Colors.ForeG.yellow}Could not load dependency {names[currentItem]}.{Colors.reset}')
                    Log(logFile, 'err', f'Could not load dependency {names[currentItem]}.')
                    autoInstall = input('Would you like to attempt an autoinstall? <Y/n> ')
                    if autoInstall.lower() == 'y':
                        # Run the given installation command and log it as debug
                        Log(logFile, 'debug', f'Attempting autoinstall of {names[currentItem]} with command'
                                              f' "{installs[currentItem]}."')
                        process = subprocess.Popen(installs[currentItem], shell=True, stdout=subprocess.PIPE)
                        process.wait()
                        # If successful, close the program.
                        if process.returncode == 0:
                            print(f'{Colors.ForeG.green}Installed dependency {names[currentItem]} successfully. '
                                  f'Continuing...{Colors.reset}')
                            Log(logFile, 'info', f'Installed dependency {names[currentItem]} successfully.')

                        # If unsuccessful, give name and install command of the module, then exit.
                        else:
                            print(f'{Colors.ForeG.red}Install failed. If you wish to attempt a manual installation, '
                                  f'the name of the module is {names[currentItem]}, and the install command should be'
                                  f'"{installs[currentItem]}".{Colors.reset}')
                            Log(logFile, 'err', f'Failed to autoinstall dependency {names[currentItem]}. Command '
                                                f'exited with code "{process.returncode}."')
                            input('Press Enter to exit...')
                            quit()

                    # If user does not attempt autoinstall, exit
                    else:
                        print(f'{Colors.ForeG.red}Cannot continue without dependency "{names[currentItem]}."'
                              f'{Colors.reset}')
                        input('Press Enter to exit...')
                        quit()

        # If any of the three lists are empty, exit
        else:
            print(f'{Colors.ForeG.red}Dependency file is empty, for some reason. Unable to continue.{Colors.reset}')
            input('Press Enter to exit...')
            quit()
