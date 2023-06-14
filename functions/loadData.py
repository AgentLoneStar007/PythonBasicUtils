## Configuration loading system by AgentLoneStar007
## https://github.com/AgentLoneStar007

import json


def loadConfig():
    # Try to load the config. If the process succeeds, return a dictionary with the config
    try:
        import yaml

        file = open('config.yml', 'r')
        config = yaml.safe_load(file)
        file.close()
        return config

    # If failed, return false
    except:
        return False


def loadAppData():
    with open('data/app.json', 'r') as file:
        app = json.load(file)
        file.close()
        return app
