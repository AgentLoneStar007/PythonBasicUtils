import os
from functions.logger import Log


class CreateDefaultConfig:
    def __init__(self, logFile):
        defaultConfig = '''# Enable this option to log more verbose output. Makes debugging easier. 
debug: false
'''

        if not os.path.isfile('config.yml'):
            Log(logFile, 'warn', 'No config file present. Creating one...')
            config = open('config.yml', 'a')
            config.write(defaultConfig)
            config.close()

        else:
            return
