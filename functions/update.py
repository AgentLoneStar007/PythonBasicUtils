import requests
from functions.loadData import loadAppData
from functions.logger import Log
from data.colors import Colors


class CheckForUpdates:
    def __init__(self, serverURL: str, logFile: str):
        # Get the current program version
        currentVersion = loadAppData()['version']
        appType = loadAppData()['app-type']
        appName = loadAppData()['name']

        # Get the info on the latest release from the server URL
        response = requests.get(serverURL)
        for x in response.json():
            print(x['tag_name'])

        #x = x.json()[0]
        #x = x.lower().replace('version', '')
        #if 'v' in x.lower():
        #    x = x.lower().replace('v', '')
        #latestVersion = x#.lower()
        #print(latestVersion)
        #latestVersionDownload =

        #if float(latestVersion) > float(currentVersion):
        #    if appType == 'graphical':
        #        return
        #    else:
        #        Log(logFile, 'info', f'Update {latestVersion} is available! (Current version is {currentVersion}.)')
        #        print(f'{Colors.ForeG.lightGreen}Version {latestVersion} of {appName} is available!')
        #        doUpdate = input(f'Would you like to install it? <Y/n> {Colors.reset}')
        #        if doUpdate.lower() == 'y':
        #            return

        #else:
        #    return

