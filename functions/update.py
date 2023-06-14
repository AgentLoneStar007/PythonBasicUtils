import re
from functions.loadData import loadAppData, loadConfig
from functions.logger import Log
from data.colors import Colors


class CheckForUpdates:
    def __init__(self, serverURL: str, logFile: str):
        # Dependencies marked as optional must be imported in a try-except block
        try:
            import requests
            from git import repo
        except Exception as e:
            print(f'{Colors.ForeG.yellow}Update functionality unavailable. Failed to import one or both of the required'
                  f' dependencies(Requests, GitPython).{Colors.reset}'
                  )
            Log(logFile, 'err', 'Failed to import one or more of the required dependencies(Requests, GitPython) for '
                                f'update functionality with the following error: {e}')
            return

        # Get the current app name, type, and version
        appName = loadAppData()['name']
        appType = loadAppData()['app-type']
        currentVersion = loadAppData()['version']

        # See if user wants beta updates
        config = loadConfig()
        includeBetas = config['participateInBetas']

        # Get the info on the latest release from the server URL
        #response = requests.get(serverURL)
        #response.json():
        #print(x['tag_name'])
        versionsList = ['v0.1-alpha', 'version0.3-beta', '0.8-pre_release', '0.9', 'v1.2', 'version-1.4', 'version_1.5',
                        'version1.6-pre-release', '1.8', '1.8.1-beta']

        # "versions" list contains version numbers. "versionTypes" list contains booleans stating whether version is
        # beta or not.
        versions = []
        versionTypes = []

        # Iterate over every version in available versions
        for x in versionsList:
            # If your releases have funky stuff in the version name, I would recommend using RegEx to remove it
            # so this update system is compatible with it.

            # Format the version name so that any junk is removed and it's lowercase
            x = x.lower()
            x = re.sub(r'^(?:version[-_]?|v[-_]?)', '', x)

            # If the version is alpha, beta, or pre-release, mark it as beta
            if bool(re.search(r'(?:prerelease|pre[-_]?release|alpha|beta)[-_]?', x)):
                x = re.sub(r'(?:prerelease|pre[-_]?release|alpha|beta)[-_]?', '', x).rstrip('-_')
                versionTypes.append(True)

            # Otherwise, mark it as stable
            else:
                versionTypes.append(False)

            # Add the version to the versions list
            versions.append(x)

        # Function that compares two versions, stating whether one is newer than another, or that they're the same
        def checkIfUpdateAvailable(version1, version2):
            # Split the version at the decimal point, and append the numbers to a list - top is current, bottom is
            # newest
            v1_parts = version1.split('.')
            v2_parts = version2.split('.')

            # Compare the numbers in the version number
            for i in range(max(len(v1_parts), len(v2_parts))):
                v1_val = int(v1_parts[i]) if i < len(v1_parts) else 0
                v2_val = int(v2_parts[i]) if i < len(v2_parts) else 0

                # If one version is newer than another, return True
                if v1_val < v2_val:
                    return True

            # Otherwise, return False
                elif v1_val > v2_val:
                    return False

            else:
                return False

        # Function that iterates over the entire version list to see what the latest version is, excluding betas if
        # requested
        def getNewestVersion():
            filteredVersions = [version for version, beta in zip(versions, versionTypes) if includeBetas or not beta]
            returnedVersion = max(filteredVersions) if filteredVersions else None

            return returnedVersion

        # Assign newest version variable
        newestVersion = getNewestVersion()

        # If update is available, proceed with update dialogue, depending on whether app is terminal or graphical
        if checkIfUpdateAvailable(currentVersion, newestVersion):
            print('Update available!')


