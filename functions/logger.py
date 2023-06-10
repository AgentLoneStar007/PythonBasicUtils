## Logging system by AgentLoneStar007
## https://github.com/AgentLoneStar007

from datetime import datetime
import os
from functions.loadData import loadConfig


def formatInput(typeInput):
    if typeInput == 'WARN':
        return 'WARNING'
    if typeInput == 'ERR':
        return 'ERROR'
    else:
        return 'INFO'


def logFileSort(inp):
    if '_' in inp:
        return int(inp[inp.index("_") + 1:-4])
    else:
        return 0


def setCurrentFile():
    # Load the folder to log to from config, if loaded
    config = loadConfig()
    if config:
        logFolder = config['logFolder']
    else:
        logFolder = 'logs'

    # If there is not a logs folder, create it
    if not os.path.exists(logFolder):
        os.makedirs(logFolder)

    # Set current date var
    now = datetime.now()
    logFileTime = now.strftime('%m-%d-%Y')

    # Create an array and append all logs in the log folder to it
    existingLogs = []
    for x in os.listdir(logFolder):
        if x.endswith('.log'):
            try:
                # Only add it if the first date given(month) is between 1 and 12. This will work even if the file
                # doesn't have the correct naming scheme
                if 1 <= int(x[:2]) <= 12:
                    existingLogs.append(x)
            except:
                continue

    # If there are logs in the log folder...
    if len(existingLogs) > 0:
        # Create another array, and append all logs in the existingLogs array in it that have the same date
        logsWithCurrentDate = []
        for x in existingLogs:
            if logFileTime in x:
                logsWithCurrentDate.append(x)
        # If there is only one log in the list, return the name {current date}_1.log
        if len(logsWithCurrentDate) == 1:
            del existingLogs
            del logsWithCurrentDate
            return f'{logFileTime}_1.log'
        # Otherwise, return the log name {current date}_{log number from last log + 1}.log
        elif len(logsWithCurrentDate) > 1:
            # Sort the array so that logs in the logsWithCurrentDate array are ordered by their number at the end
            logsWithCurrentDate.sort(key=logFileSort)
            # Create a var of the name of the last created log
            currentDateLog = logsWithCurrentDate[-1]
            # Set the log number to be appended at the end of the log name to be plus one from the last log
            logNumber = f'{int(currentDateLog[currentDateLog.index("_") + 1:-4]) + 1}'
            del existingLogs
            del logsWithCurrentDate
            return f'{logFileTime}_{logNumber}.log'
    del existingLogs
    return f'{logFileTime}.log'


class Log:
    def __init__(self, logFile, infoType, message):
        # Create current time var
        now = datetime.now()
        currentTime = now.strftime('[%m/%d/%Y-%H:%M:%S]')

        # Format input in case something stupid was used like 'err' for error.
        infoType = infoType.upper()
        infoTypes = ['INFO', 'WARNING', 'ERROR', 'DEBUG']
        if infoType not in infoTypes:
            infoType = formatInput(infoType)

        # Check if config is loaded. If not, log debugs by default. If so, load config.
        config = loadConfig()
        if config:
            logDebug = config['debug']
            logFolder = config['logFolder']
        else:
            logDebug = True
            logFolder = 'logs'

        with open(f'{logFolder}/{logFile}', 'a+') as logFile:
            if infoType == 'DEBUG' and logDebug:
                logFile.write(f'{currentTime} <{infoType}>: {message}\n')
            if infoType != 'DEBUG':
                logFile.write(f'{currentTime} <{infoType}>: {message}\n')
