## Configuration loading system by AgentLoneStar007
## https://github.com/AgentLoneStar007

import json

def loadConfig():
    try:
        import yaml

        file = open('config.yml', 'r')
        config = yaml.safe_load(file)
        return config

    except:
        return False


def loadAppData():
    with open('data/app.json', 'r') as file:
        app = json.load(file)
        file.close()
        return app
