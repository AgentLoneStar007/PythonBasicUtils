## Configuration loading system by AgentLoneStar007
## https://github.com/AgentLoneStar007

class LoadConfig:
    # Main function(has a return value so can't be __init__)
    def isConfigLoaded(self):
        try:
            import yaml

            file = open('config.yml', 'r')
            config = yaml.safe_load(file)
            return config

        except:
            return False
