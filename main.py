from functions.installDependencies import InstallDependencies
from functions.createDefaultConfig import CreateDefaultConfig
from functions.logger import setCurrentFile
from functions.loadConfig import LoadConfig


class Main:
    def __init__(self):
        # Order of events:
        # 1. Set file to log to
        # 2. Create the default configuration file, if not present already.
        # 3. Install dependencies.
        # 4. Load the configuration file.

        currentLogFile = setCurrentFile()

        CreateDefaultConfig(currentLogFile)
        InstallDependencies(currentLogFile)


Main()
