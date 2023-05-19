## Configuration loading system by AgentLoneStar007
## https://github.com/AgentLoneStar007

def loadConfig():
    try:
        import yaml

        file = open('config.yml', 'r')
        config = yaml.safe_load(file)
        return config

    except:
        return False
