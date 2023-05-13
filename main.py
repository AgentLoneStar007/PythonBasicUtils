## Credit for Config, Dependency Installation, and Logging systems goes to AgentLoneStar007
## https://github.com/AgentLoneStar007

from functions.installDependencies import InstallDependencies
from functions.createDefaultConfig import CreateDefaultConfig
from functions.logger import setCurrentFile  # Import Log as well if you wish to log anything in Main.


class Main:
    def __init__(self):
        # Order of events:
        # 1. Set file to log to (must be passed through to all functions and classes logging output)
        # 2. Create the default configuration file, if not present already.
        # 3. Install dependencies.
        # 4. Load the configuration file.

        currentLogFile = setCurrentFile()

        CreateDefaultConfig(currentLogFile)
        InstallDependencies(currentLogFile)

        # Your code here. Don't forget to pass the log file through to your classes and functions.


Main()
