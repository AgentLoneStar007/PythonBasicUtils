import requests
import re
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
        #response = requests.get(serverURL)
        #response.json():
        versionsList = ['v0.1-alpha', 'version0.3-beta', '0.8-pre_release', '0.9', 'v1.2', 'version-1.4', 'version_1.5',
                    'version1.6-pre-release']
        versions = {}
        for x in versionsList:
            #print(x['tag_name'])
            x = x.lower()
            x = re.sub(r'^(?:version[-_]?|v[-_]?)', '', x)

            if bool(re.search(r'(?:prerelease|pre[-_]?release|alpha|beta)[-_]?', x)):
                x = re.sub(r'(?:prerelease|pre[-_]?release|alpha|beta)[-_]?', '', x).rstrip('-_')
                versions[x] = 'beta'

            else:
                versions[x] = 'stable'

        print(versions)

